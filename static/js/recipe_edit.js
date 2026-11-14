// Function to update step numbers
function updateStepNumbers() {
  // Select only visible step forms (those not having the 'form-hidden' class)
  const stepForms = document.querySelectorAll('#step-formset .step-form:not(.form-hidden)');
  stepForms.forEach((form, index) => {
    const numberSpan = form.querySelector('.step-number');
    if (numberSpan) {
      numberSpan.textContent = (index + 1) + '.';
    }
  });
}

// Function to add a new form to a formset
function addForm(formsetType, containerSelector, totalFormsSelector, emptyFormSelector) {
  const container = document.querySelector(containerSelector);
  const totalFormsInput = document.querySelector(totalFormsSelector);
  const emptyFormTemplate = document.querySelector(emptyFormSelector).innerHTML;
  const formCount = parseInt(totalFormsInput.value);

  const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
  const tempContainer = document.createElement('template');
  tempContainer.innerHTML = newFormHtml.trim();
  const newFormElement = tempContainer.content.firstChild;


  if (newFormElement) {
    container.appendChild(newFormElement); // Append the actual form element
  } else {
    console.error("Could not create new form element from template:", newFormHtml);
    return; // Exit if element creation failed
  }

  totalFormsInput.value = formCount + 1;

  // Update step numbers if adding a step
  if (formsetType === 'step') {
    updateStepNumbers();
  }
}

// Function to handle form removal (shared by delegated listeners)
function handleRemoveForm(event) {
  // Check if the clicked element is actually the remove button
  if (!event.target.classList.contains('remove-form')) {
    return; // Exit if the click wasn't on a remove button
  }

  const button = event.target;
  const formToRemove = button.closest('.ingredient-form, .tag-form, .step-form');
  if (!formToRemove) return; // Exit if form container not found

  console.log("Attempting to remove form:", formToRemove); // Log the form being targeted

  const deleteCheckbox = formToRemove.querySelector('input[type="checkbox"][name$="-DELETE"]');

  if (deleteCheckbox) {
    // If a delete checkbox exists (meaning the form corresponds to an existing object),
    // check the box and add the hiding class.
    console.log("Found DELETE checkbox, hiding form using class."); // Log action
    deleteCheckbox.checked = true;
    formToRemove.classList.add('form-hidden'); // Added class
  } else {
    // If it's a newly added form (no delete checkbox), remove it from the DOM.
    console.log("No DELETE checkbox found, removing form from DOM."); // Log action
    formToRemove.remove();
  }

  // Update step numbers if removing/hiding a step form
  if (formToRemove.classList.contains('step-form')) {
    console.log("Updating step numbers."); // Log action
    updateStepNumbers();
  }
}

// --- Event Listeners ---

// Add Form Buttons
document.getElementById('add-ingredient').addEventListener('click', function () {
  addForm('ingredient', '#ingredient-formset', '#id_ingredient_set-TOTAL_FORMS', '#ingredient-empty-form');
});

document.getElementById('add-tag').addEventListener('click', function () {
  addForm('tag', '#tag-formset', '#id_tag_set-TOTAL_FORMS', '#tag-empty-form');
});

document.getElementById('add-step').addEventListener('click', function () {
  addForm('step', '#step-formset', '#id_step_set-TOTAL_FORMS', '#step-empty-form');
});

// Remove Form Buttons (using Event Delegation)
document.getElementById('ingredient-formset').addEventListener('click', handleRemoveForm);
document.getElementById('tag-formset').addEventListener('click', handleRemoveForm);
document.getElementById('step-formset').addEventListener('click', handleRemoveForm);


// Initial update of step numbers on page load
document.addEventListener('DOMContentLoaded', function () {
  updateStepNumbers();

  // Also update step numbers if any existing forms are marked for deletion on load
  // (e.g., if validation failed on a previous submission with forms deleted)
  document.querySelectorAll('#step-formset .step-form input[type="checkbox"][name$="-DELETE"]:checked').forEach(checkbox => {
    checkbox.closest('.step-form').classList.add('form-hidden');
  });
  updateStepNumbers(); // Call again after hiding
});


document.addEventListener('DOMContentLoaded', function () {
  const imageUploadInput = document.getElementById('id_image_upload'); // Input for choosing the file
  const imageToCropElement = document.getElementById('image-to-crop'); // <img> tag where the selected image is shown for cropping
  const imageCropContainer = document.getElementById('image-crop-container'); // Container for the image-to-crop
  const cropButton = document.getElementById('crop-button'); // Button to trigger the crop action
  const croppedImageDataInput = document.getElementById('id_image_data_uri'); // Hidden input to store the Data URI
  const croppedPreviewContainer = document.getElementById('cropped-preview-container'); // Container for the preview
  const croppedPreview = document.getElementById('cropped-preview'); // <img> tag for the cropped preview

  let cropper = null; // Variable to store the Cropper.js instance

  // --- Image Cropper Logic ---

  if (imageUploadInput && imageToCropElement && imageCropContainer && cropButton && croppedImageDataInput && croppedPreviewContainer && croppedPreview) {

    // Add an event listener to the image element to initialize cropper after it loads
    imageToCropElement.addEventListener('load', function () {
      // Ensure previous cropper instance is destroyed if it exists
      if (cropper) {
        cropper.destroy();
      }

      // Initialize Cropper.js on the loaded image
      cropper = new Cropper(imageToCropElement, {
        aspectRatio: 1 / 1, // Square
        viewMode: 1, // Cropper view mode (restrict crop box to canvas)
        background: false, // Transparent background for cropper (refers to the main container background)
        responsive: true,
        minContainerWidth: 200,
        minCropBoxWidth: 200,
        movable: false, // Set to true if you want the cropped area movable
        zoomOnTouch: false, // Set to true if you want zoom on touch devices
        zoomOnWheel: false, // Set to true if you want zoom with mouse wheel
      });

      // Show the image container and crop button now that the image is loaded and cropper is initialized
      imageCropContainer.style.display = 'block';
      cropButton.style.display = 'inline-block';
      croppedPreviewContainer.style.display = 'none'; // Hide previous preview
    });

    imageUploadInput.addEventListener('change', function (event) {
      const files = event.target.files;
      if (files && files.length > 0) {
        const reader = new FileReader();
        reader.onload = function (e) {
          // Set the source of the image element.
          // The 'load' event listener on the image will handle initialization.
          imageToCropElement.src = e.target.result;
        };
        reader.readAsDataURL(files[0]);
      }
    });

    cropButton.addEventListener('click', function () {
      if (cropper) {
        const canvas = cropper.getCroppedCanvas();

        if (!canvas) {
          alert('Could not crop the image. Please try again.');
          return;
        }

        // Get the data URI of the cropped image
        // Note: You can specify the image format and quality here (e.g., 'image/jpeg', 0.9 for JPEG quality)
        const croppedDataURL = canvas.toDataURL('image/png', 1.0); // PNG format with full quality

        // Set the value of the hidden input field
        croppedImageDataInput.value = croppedDataURL;

        // Show the preview of the cropped image
        croppedPreview.src = croppedDataURL;
        croppedPreviewContainer.style.display = 'block';

        // Optional: Hide the cropper interface after successful crop
        imageCropContainer.style.display = 'none';
        cropButton.style.display = 'none';
        if (cropper) {
            cropper.destroy(); // Clean up the cropper instance
            cropper = null;
        }
        alert('Image cropped! It will be saved with the recipe.');
      } else {
        alert('Please select an image to crop first.');
      }
    });

    // Handle existing image Data URI if editing a recipe
    // Assumes `window.existingImageDataUri` is set by your Django template
    if (typeof window.existingImageDataUri !== 'undefined' && window.existingImageDataUri) {
      // Set the source for the preview directly since no cropping is needed initially
      croppedPreview.src = window.existingImageDataUri;
      croppedPreviewContainer.style.display = 'block';
      // Optionally, also set the hidden input's value
      croppedImageDataInput.value = window.existingImageDataUri;
    }


  } else {
    console.warn("One or more image cropper elements are missing from the DOM.");
  }
});