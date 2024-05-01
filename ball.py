import cv2

backSub = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(2)

def nearEdge(x, y, w, h, frame):
    width = frame.shape[1]
    height = frame.shape[0]

    distLeftWall = x
    distRightWall = width - (x + w)
    distTopWall = y
    distBottomWall = height - (y + h)

    if distLeftWall < 20 or distRightWall < 20:
        return True
    
    if distTopWall < 20 or distBottomWall < 20:
        return True
    
    return False

while True:
    ret, frame = cap.read()
    fgMask = backSub.apply(frame)

    contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # ignore small boxes
        if w < 20 or h < 20:
            continue

        # ignore boxes not near edges
        if not nearEdge(x, y, w, h, frame):
            continue

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detected Objects', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()