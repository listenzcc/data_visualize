// Metric functions
// Compute the new circle position based on input,
// the new circle will cut with the given two circles.
//  Args:
//  - @p1: The first circle;
//  - @p2: The second circle;
//  - @r3: The radius of the new circle.
//  Returns:
//  - The point of the new circle.
//  Others:
//    The point is structured as [x, y, r]
//    - x is the x position of the center;
//    - y is the y position of the center;
//    - r is the radius of the circle.
function rightCircle(p1, p2, r3) {
    const x1 = p1[0],
        y1 = p1[1],
        r1 = p1[2];

    const x2 = p2[0],
        y2 = p2[1],
        r2 = p2[2];

    const a = r2 + r3,
        b = r1 + r3,
        c = distance(p1, p2);

    if (c > a + b) {
        return [0, 0, r3];
    }

    const dx = (x2 - x1) / c,
        dy = (y2 - y1) / c;

    const odx = -dy,
        ody = dx;

    const aa = acos((b ** 2 + c ** 2 - a ** 2) / 2 / b / c);

    const co = cos(aa) * b,
        si = sin(aa) * b;

    return [x1 + co * dx + si * odx, y1 + co * dy + si * ody, r3];
}

// Compute the distance between p1 and p2
function distance(p1, p2) {
    const x1 = p1[0],
        y1 = p1[1];

    const x2 = p2[0],
        y2 = p2[1];

    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

// Compute if the circle of p1 and p2 is conflict
function conflict(p1, p2) {
    const r1 = p1[2];

    const r2 = p2[2];

    return distance(p1, p2) < r1 + r2 - 1;
}
