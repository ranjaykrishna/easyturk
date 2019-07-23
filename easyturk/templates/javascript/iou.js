var ETJS = (function(etjs) {

	etjs.intersection_over_union = function(bbox, other) {
    /** Calculates IoU between two bboxes.
     * 
     * Args:
     *     bbox: A bbox dictionary with x, y, w, h.
     *     other: Same as bbox.
     *
     * Returns:
     *     IoU between bbox and other.
     **/
		if (!bbox || !other) return 0;
		var x1 = Math.max(bbox['x'], other['x']);
		var x2 = Math.min(bbox['x'] + bbox['w'],
							other['x'] + other['w']);
		var y1 = Math.max(bbox['y'], other['y']);
		var y2 = Math.min(bbox['y'] + bbox['h'],
							other['y'] + other['h']);
		if (x1 > x2 || y1 > y2) return 0;
		var a1 = bbox['w'] * bbox['h'];
		var a2 = other['w'] * other['h'];
		var o = (x2 - x1) * (y2 - y1);
		var iou = o / (a1 + a2 - o + 1e-9); 
		return iou;
	};

return etjs;
}(ETJS || {}));
