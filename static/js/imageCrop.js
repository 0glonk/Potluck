document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const croppedImage = document.getElementById('croppedImage');
    const cropButton = document.getElementById('cropButton');

    let cropper

    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                croppedImage.src = e.target.result;

                cropper = new Cropper(croppedImage, {
                    aspectRatio: 1,
                    viewMode: 1,
                    minContainerWidth: 200,
                    minCropBoxWidth: 200,
                    movable: false,
                    zoomOnTouch: false,
                    zoomOnWheel: false,
                })
            };
            reader.readAsDataURL(file);
        }
    });

    cropButton.addEventListener('click', function() {
        const croppedDataUrl = cropper.getCroppedCanvas().toDataURL("image/png");
        console.log(croppedDataUrl);
        document.getElementById('id_imageURL').value = croppedDataUrl;
    });
});

