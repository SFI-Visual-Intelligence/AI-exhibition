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

    /*function detectPose() {
        net.estimateSinglePose(video, {
            flipHorizontal: false
        }).then(pose => {
            drawPose(pose);
            requestAnimationFrame(detectPose);
        });*/
    // Function for multiple poses
    function detectPose() {
        net.estimateMultiplePoses(video, {
            flipHorizontal: false,
            maxDetections: 5,  // Adjust this value based on expected number of people
            scoreThreshold: 0.5,
            nmsRadius: 20  // Adjust non-max suppression radius if needed
        }).then(poses => {
            drawPoses(poses);
            requestAnimationFrame(detectPose);
        });
    }
    

    function drawPoses(poses) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'red'; // Here you change the color of the circle
        ctx.strokeStyle = 'white'; // Here you change the color of the line 
        ctx.lineWidth = 10; // Here you change the width of the line 
        // List of eye keypoints
        const eyePoints = ['leftEye', 'rightEye'];
        
        poses.forEach(pose => {

            pose.keypoints.forEach((point,index) => {
                if ((point.score > 0.5 && eyePoints.includes(point.part))) {
                    ctx.beginPath();
                    ctx.arc(point.position.x, point.position.y, 10, 0, 2 * Math.PI); // radius = 5 here
                    ctx.fill();
                    
                }
            });

            // Define the skeleton connections
            const adjacentKeyPoints = posenet.getAdjacentKeyPoints(pose.keypoints, 0.5);

            //adjacentKeyPoints.forEach((keypoints) => {
            //    ctx.beginPath();
            //    ctx.moveTo(keypoints[0].position.x, keypoints[0].position.y);
            //    ctx.lineTo(keypoints[1].position.x, keypoints[1].position.y);
            //    ctx.stroke();  
            //});

            // Draw bones
            adjacentKeyPoints.forEach((keypoints) => {
                const gradient = ctx.createLinearGradient(keypoints[0].position.x, keypoints[0].position.y, keypoints[1].position.x, keypoints[1].position.y);
                gradient.addColorStop(0, "white");
                gradient.addColorStop(0.5, "gray");
                gradient.addColorStop(1, "white");

                ctx.strokeStyle = gradient;
                ctx.lineWidth = 10;
                ctx.lineCap = 'round';  // This makes the ends of the line rounded

                ctx.beginPath();
                ctx.moveTo(keypoints[0].position.x, keypoints[0].position.y);
                ctx.lineTo(keypoints[1].position.x, keypoints[1].position.y);
                ctx.stroke();
            });


            // Get keypoints for shoulders and hips
            const leftShoulder = pose.keypoints.find(point => point.part === 'leftShoulder');
            const rightShoulder = pose.keypoints.find(point => point.part === 'rightShoulder');
            const leftHip = pose.keypoints.find(point => point.part === 'leftHip');
            const rightHip = pose.keypoints.find(point => point.part === 'rightHip');

            if (leftShoulder && rightShoulder && leftHip && rightHip &&
                leftShoulder.score > 0.5 && rightShoulder.score > 0.5 &&
                leftHip.score > 0.5 && rightHip.score > 0.5) {
                
                const numRibs = 10;

                // Display ribs
                for (let i = 0; i <= numRibs; i++) {
                    const fraction = i / numRibs;
                    const startX = leftShoulder.position.x + fraction * (leftHip.position.x - leftShoulder.position.x)/2;
                    const startY = leftShoulder.position.y + fraction * (leftHip.position.y - leftShoulder.position.y)/2;
                    const endX = rightShoulder.position.x + fraction * (rightHip.position.x - rightShoulder.position.x)/2;
                    const endY = rightShoulder.position.y + fraction * (rightHip.position.y - rightShoulder.position.y)/2;

                    ctx.beginPath();
                    ctx.moveTo(startX, startY);
                    ctx.lineTo(endX, endY);
                    ctx.strokeStyle = 'gray';
                    ctx.lineWidth = 5;
                    ctx.stroke();
                }
                // Calculer le milieu des épaules et des hanches
                const midShoulderX = (leftShoulder.position.x + rightShoulder.position.x) / 2;
                const midShoulderY = (leftShoulder.position.y + rightShoulder.position.y) / 2;
                const midHipX = (leftHip.position.x + rightHip.position.x) / 2;
                const midHipY = (leftHip.position.y + rightHip.position.y) / 2;

                // Dessiner la colonne vertébrale
                ctx.beginPath();
                ctx.moveTo(midShoulderX, midShoulderY);
                ctx.lineTo(midHipX, midHipY);
                ctx.strokeStyle = 'gray';
                ctx.lineWidth = 10;
                ctx.stroke();
            }
        });
    }

    detectPose();
}

loadAndPredict();