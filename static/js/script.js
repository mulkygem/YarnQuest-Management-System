document.addEventListener('DOMContentLoaded', function () {
  const locateBtn = document.getElementById('locateBtn');
  const locationOutput = document.getElementById('locationOutput');

  if (locateBtn) {
    locateBtn.addEventListener('click', function () {
      if (!navigator.geolocation) {
        locationOutput.textContent = 'Geolocation is not supported by your browser.';
        return;
      }

      locationOutput.textContent = 'Getting your current location...';
      navigator.geolocation.getCurrentPosition(
        function (position) {
          locationOutput.innerHTML = `Your location: <strong>${position.coords.latitude.toFixed(5)}, ${position.coords.longitude.toFixed(5)}</strong>`;
        },
        function () {
          locationOutput.textContent = 'Unable to retrieve your location. Please allow location access in your browser.';
        }
      );
    });
  }
});
