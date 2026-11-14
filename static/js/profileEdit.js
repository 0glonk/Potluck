const popupButtons = document.querySelectorAll('.edit-popup-btn');
const settingsPopup = document.getElementById('settingsPopup');

// account settings menu pop up 
const acctSettingsBtn = document.getElementById('accountSettingsBtn');
const acctSettingsPopup = document.getElementById('acctSettingsPopup');
const acctSettingsOverlay = document.getElementById('acctSettingsOverlay');
const acctSettingsCancelBtn = document.getElementById('acctSettingsCancelBtn');

document.addEventListener('DOMContentLoaded', function () {
  // Enables togglers for editing profile information
  document.getElementById("editNameBtn").addEventListener("click", function () {
    const usernameField = document.getElementById("usernameField");
    usernameField.disabled = !usernameField.disabled;
    usernameField.focus();
  });

  document.getElementById("editBioBtn").addEventListener("click", function () {
    const bioField = document.getElementById("bioField");
    bioField.disabled = !bioField.disabled;
    bioField.focus();
  });

  // Saves the updated bio
  document.getElementById('formSubmit').addEventListener('click', async () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch('/account/update-profile/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
      },
      body: new URLSearchParams({
        'username': usernameField.value,
        'bio': bioField.value
      })
    });

    const data = await response.json();

    if (data.status === 'success') {
      usernameField.disabled = true;
      bioField.disabled = true;
      alert("Profile updated!");
    } else {
      alert("Error updating profile.");
    }
  });


  // Show popup
  function openPopup() {
    settingsPopup.style.display = 'block';
    overlay.style.display = 'block';
  }

  // Hide popup
  function closePopup() {
    settingsPopup.style.display = 'none';
    overlay.style.display = 'none';
  }

  // Attach click to each popup trigger button
  popupButtons.forEach(button => {
    button.addEventListener('click', openPopup);
  });

  // Profile Image Update
  const editProfileImageBtn = document.getElementById('editProfileImageBtn');

  editProfileImageBtn.addEventListener('click', function () {
    alert("Profile image editing will be available soon!");
  });



  acctSettingsBtn.addEventListener('click', () => {
    acctSettingsPopup.style.display = 'block';
    acctSettingsOverlay.style.display = 'block';
  });

  acctSettingsCancelBtn.addEventListener('click', () => {
    acctSettingsPopup.style.display = 'none';
    acctSettingsOverlay.style.display = 'none';
  });

  acctSettingsOverlay.addEventListener('click', () => {
    acctSettingsPopup.style.display = 'none';
    acctSettingsOverlay.style.display = 'none';
  });
});


function showUserRecipes() {
  // Tabs
  document.querySelector('.recipe-tab:nth-child(1)').classList.add('active-tab');
  document.querySelector('.recipe-tab:nth-child(2)').classList.remove('active-tab');

  // Content
  document.getElementById('user_recipes').classList.remove('hidden');
  document.getElementById('bookmarked_recipes').classList.add('hidden');
}

function showBookmarkedRecipes() {
  // Tabs
  document.querySelector('.recipe-tab:nth-child(1)').classList.remove('active-tab');
  document.querySelector('.recipe-tab:nth-child(2)').classList.add('active-tab');

  // Content
  document.getElementById('user_recipes').classList.add('hidden');
  document.getElementById('bookmarked_recipes').classList.remove('hidden');
}

