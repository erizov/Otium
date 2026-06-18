# -*- coding: utf-8 -*-
"""Offline person/animal main-subject filter for guide place images."""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_MODEL_URLS: tuple[str, ...] = (
    # Ultralytics assets release URLs can change; keep a small fallback list.
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8n.onnx",
    "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.onnx",
)
_MODEL_CACHE = Path(__file__).resolve().parent / ".cache" / "yolov8n.onnx"
_INPUT_SIZE = 640
_PERSON_CLASS = 0
_ANIMAL_CLASSES = frozenset(range(14, 24))
_CONF_THRESHOLD = 0.35
_IOU_THRESHOLD = 0.45

# Normal thresholds (fraction of image area).
_PERSON_MAIN_AREA = 0.10
_PERSON_CENTER_AREA = 0.05
_ANIMAL_MAIN_AREA = 0.10
_CROWD_EACH_AREA = 0.03
_CROWD_MIN_COUNT = 3
_CROWD_TOTAL_PERSON_AREA = 0.15
_CENTER_LO = 0.25
_CENTER_HI = 0.75

_SESSION: Any = None
_WARNED_UNAVAILABLE = False


@dataclass(frozen=True)
class SubjectFilterResult:
    accept: bool
    reason: str = ""
    person_area_ratio: float = 0.0
    animal_area_ratio: float = 0.0
    person_count: int = 0


def subject_filter_enabled() -> bool:
    """On by default; set ``SUBJECT_FILTER=0`` to disable."""
    raw = os.environ.get("SUBJECT_FILTER", "1").strip().lower()
    return raw not in ("0", "false", "no", "off")


def subject_filter_strict() -> bool:
    raw = os.environ.get("SUBJECT_FILTER_STRICT", "").strip().lower()
    return raw in ("1", "true", "yes")


def _fail_open() -> bool:
    raw = os.environ.get("SUBJECT_FILTER_FAIL_OPEN", "1").strip().lower()
    return raw not in ("0", "false", "no")


def _thresholds() -> dict[str, float]:
    if subject_filter_strict():
        return {
            "person_main": 0.06,
            "person_center": 0.03,
            "animal_main": 0.06,
            "crowd_each": 0.02,
            "crowd_total": 0.10,
        }
    return {
        "person_main": _PERSON_MAIN_AREA,
        "person_center": _PERSON_CENTER_AREA,
        "animal_main": _ANIMAL_MAIN_AREA,
        "crowd_each": _CROWD_EACH_AREA,
        "crowd_total": _CROWD_TOTAL_PERSON_AREA,
    }


def _box_area_ratio(x1: float, y1: float, x2: float, y2: float, area: float) -> float:
    if area <= 0:
        return 0.0
    return max(0.0, (x2 - x1) * (y2 - y1) / area)


def _center_in_core(
    cx: float,
    cy: float,
    img_w: int,
    img_h: int,
) -> bool:
    nx = cx / float(img_w)
    ny = cy / float(img_h)
    return _CENTER_LO <= nx <= _CENTER_HI and _CENTER_LO <= ny <= _CENTER_HI


def evaluate_detections(
    detections: list[tuple[int, float, float, float, float, float]],
    img_w: int,
    img_h: int,
) -> SubjectFilterResult:
    """
    Decide accept/reject from detections.

    Each item: (class_id, x1, y1, x2, y2, confidence).
    """
    area = float(img_w * img_h)
    if area <= 0:
        return SubjectFilterResult(accept=True)

    thr = _thresholds()
    person_areas: list[float] = []
    animal_max = 0.0

    for cls_id, x1, y1, x2, y2, _conf in detections:
        ratio = _box_area_ratio(x1, y1, x2, y2, area)
        if cls_id == _PERSON_CLASS:
            person_areas.append(ratio)
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            if ratio >= thr["person_main"]:
                return SubjectFilterResult(
                    accept=False,
                    reason="person_main",
                    person_area_ratio=ratio,
                    person_count=len(person_areas),
                )
            if (
                ratio >= thr["person_center"]
                and _center_in_core(cx, cy, img_w, img_h)
            ):
                return SubjectFilterResult(
                    accept=False,
                    reason="person_center",
                    person_area_ratio=ratio,
                    person_count=len(person_areas),
                )
        elif cls_id in _ANIMAL_CLASSES and ratio >= thr["animal_main"]:
            animal_max = max(animal_max, ratio)
            return SubjectFilterResult(
                accept=False,
                reason="animal_main",
                animal_area_ratio=ratio,
                person_count=len(person_areas),
            )
        elif cls_id in _ANIMAL_CLASSES:
            animal_max = max(animal_max, ratio)

    crowdish = [a for a in person_areas if a >= thr["crowd_each"]]
    total_person = sum(person_areas)
    if len(crowdish) >= _CROWD_MIN_COUNT or total_person >= thr["crowd_total"]:
        return SubjectFilterResult(
            accept=False,
            reason="crowd",
            person_area_ratio=total_person,
            person_count=len(person_areas),
        )

    return SubjectFilterResult(
        accept=True,
        person_area_ratio=max(person_areas) if person_areas else 0.0,
        animal_area_ratio=animal_max,
        person_count=len(person_areas),
    )


def _warn_unavailable(msg: str) -> None:
    global _WARNED_UNAVAILABLE
    if _WARNED_UNAVAILABLE:
        return
    _WARNED_UNAVAILABLE = True
    print("Subject filter unavailable: {}".format(msg), file=sys.stderr)


def _ensure_model() -> Path | None:
    if _MODEL_CACHE.is_file():
        return _MODEL_CACHE
    _MODEL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    last_exc: Exception | None = None
    for url in _MODEL_URLS:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "ExcursionGuide/1.0 (YOLOv8n onnx)"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                _MODEL_CACHE.write_bytes(resp.read())
            return _MODEL_CACHE
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            last_exc = exc
            continue
    _warn_unavailable("model download failed ({})".format(last_exc))
    return None


def _get_session() -> Any | None:
    global _SESSION
    if _SESSION is not None:
        return _SESSION
    try:
        import onnxruntime as ort
    except ImportError:
        _warn_unavailable("install onnxruntime")
        return None
    model = _ensure_model()
    if model is None:
        return None
    _SESSION = ort.InferenceSession(
        str(model),
        providers=["CPUExecutionProvider"],
    )
    return _SESSION


def _letterbox(
    image: Any,
    new_size: int = _INPUT_SIZE,
) -> tuple[Any, float, tuple[float, float]]:
    import numpy as np

    w, h = image.size
    scale = min(new_size / w, new_size / h)
    nw = int(round(w * scale))
    nh = int(round(h * scale))
    pad_x = (new_size - nw) / 2.0
    pad_y = (new_size - nh) / 2.0
    from PIL import Image

    resized = image.resize((nw, nh), Image.Resampling.BILINEAR)
    canvas = Image.new("RGB", (new_size, new_size), (114, 114, 114))
    canvas.paste(resized, (int(pad_x), int(pad_y)))
    arr = np.asarray(canvas, dtype=np.float32) / 255.0
    arr = arr.transpose(2, 0, 1)[None, ...]
    return arr, scale, (pad_x, pad_y)


def _nms(
    boxes: list[list[float]],
    scores: list[float],
    iou_thr: float,
) -> list[int]:
    if not boxes:
        return []
    import numpy as np

    order = np.argsort(scores)[::-1]
    keep: list[int] = []
    boxes_arr = np.array(boxes, dtype=np.float32)
    while order.size > 0:
        i = int(order[0])
        keep.append(i)
        if order.size == 1:
            break
        rest = order[1:]
        xx1 = np.maximum(boxes_arr[i, 0], boxes_arr[rest, 0])
        yy1 = np.maximum(boxes_arr[i, 1], boxes_arr[rest, 1])
        xx2 = np.minimum(boxes_arr[i, 2], boxes_arr[rest, 2])
        yy2 = np.minimum(boxes_arr[i, 3], boxes_arr[rest, 3])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        area_i = (boxes_arr[i, 2] - boxes_arr[i, 0]) * (
            boxes_arr[i, 3] - boxes_arr[i, 1]
        )
        area_r = (
            (boxes_arr[rest, 2] - boxes_arr[rest, 0])
            * (boxes_arr[rest, 3] - boxes_arr[rest, 1])
        )
        iou = inter / (area_i + area_r - inter + 1e-6)
        order = rest[iou <= iou_thr]
    return keep


def detect_person_animal_boxes(
    image: Any,
) -> list[tuple[int, float, float, float, float, float]]:
    """Run YOLOv8n ONNX; return boxes in original image coordinates."""
    session = _get_session()
    if session is None:
        return []

    import numpy as np

    tensor, scale, (pad_x, pad_y) = _letterbox(image)
    inp = session.get_inputs()[0].name
    out = session.run(None, {inp: tensor})[0]
    preds = np.squeeze(out).T
    scores = preds[:, 4:].max(axis=1)
    class_ids = preds[:, 4:].argmax(axis=1)
    mask = scores >= _CONF_THRESHOLD
    if not mask.any():
        return []

    boxes: list[list[float]] = []
    sc: list[float] = []
    cls: list[int] = []
    iw, ih = image.size
    for row, cid, scv in zip(preds[mask], class_ids[mask], scores[mask]):
        cid = int(cid)
        if cid != _PERSON_CLASS and cid not in _ANIMAL_CLASSES:
            continue
        cx, cy, bw, bh = row[:4]
        x1 = (cx - bw / 2.0 - pad_x) / scale
        y1 = (cy - bh / 2.0 - pad_y) / scale
        x2 = (cx + bw / 2.0 - pad_x) / scale
        y2 = (cy + bh / 2.0 - pad_y) / scale
        x1 = max(0.0, min(float(iw), x1))
        y1 = max(0.0, min(float(ih), y1))
        x2 = max(0.0, min(float(iw), x2))
        y2 = max(0.0, min(float(ih), y2))
        boxes.append([x1, y1, x2, y2])
        sc.append(float(scv))
        cls.append(cid)

    keep = _nms(boxes, sc, _IOU_THRESHOLD)
    out_boxes: list[tuple[int, float, float, float, float, float]] = []
    for i in keep:
        out_boxes.append((cls[i], *boxes[i], sc[i]))
    return out_boxes


def check_image_bytes(data: bytes) -> SubjectFilterResult:
    """Return accept=False when people/animals dominate the frame."""
    if not subject_filter_enabled():
        return SubjectFilterResult(accept=True)
    if not data or len(data) < 500:
        return SubjectFilterResult(accept=True)

    try:
        from PIL import Image
    except ImportError:
        if _fail_open():
            _warn_unavailable("Pillow missing")
            return SubjectFilterResult(accept=True)
        return SubjectFilterResult(accept=False, reason="filter_unavailable")

    try:
        image = Image.open(BytesIO(data)).convert("RGB")
    except Exception:
        return SubjectFilterResult(accept=True)

    boxes = detect_person_animal_boxes(image)
    if not boxes and _get_session() is None:
        if _fail_open():
            return SubjectFilterResult(accept=True, reason="filter_skipped")
        return SubjectFilterResult(accept=False, reason="filter_unavailable")

    return evaluate_detections(boxes, image.size[0], image.size[1])


def check_image_path(path: Path) -> SubjectFilterResult:
    if not path.is_file():
        return SubjectFilterResult(accept=False, reason="missing")
    try:
        data = path.read_bytes()
    except OSError:
        return SubjectFilterResult(accept=False, reason="read_error")
    return check_image_bytes(data)


def rejection_message(result: SubjectFilterResult) -> str:
    if result.accept:
        return "ok"
    parts = [result.reason or "rejected"]
    if result.person_area_ratio > 0:
        parts.append("person={:.1%}".format(result.person_area_ratio))
    if result.animal_area_ratio > 0:
        parts.append("animal={:.1%}".format(result.animal_area_ratio))
    if result.person_count:
        parts.append("n={}".format(result.person_count))
    return "subject filter: " + ", ".join(parts)
