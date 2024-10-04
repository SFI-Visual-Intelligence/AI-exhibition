async function setupCamera() {
    const video = document.getElementById('video');
    const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
    });
    video.srcObject = stream;

    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function loadAndPredict() {
    const video = await setupCamera();
    video.play();

    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    const net = await posenet.load();

    function detectPose() {
        net.estimateSinglePose(video, {
            flipHorizontal: false
        }).then(pose => {
            drawPose(pose);
            requestAnimationFrame(detectPose);
        });
    }

    function drawPose(pose) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'red';
        ctx.strokeStyle = 'blue';

        pose.keypoints.forEach(point => {
            if (point.score > 0.5) {
                ctx.beginPath();
                ctx.arc(point.position.x, point.position.y, 5, 0, 2 * Math.PI);
                ctx.fill();
            }
        });

        // Define the skeleton connections
        const adjacentKeyPoints = posenet.getAdjacentKeyPoints(pose.keypoints, 0.5);

        adjacentKeyPoints.forEach((keypoints) => {
            ctx.beginPath();
            ctx.moveTo(keypoints[0].position.x, keypoints[0].position.y);
            ctx.lineTo(keypoints[1].position.x, keypoints[1].position.y);
            ctx.stroke();
        });
    }

    detectPose();
}

loadAndPredict();