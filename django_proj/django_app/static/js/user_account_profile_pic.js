/* ----------------- PROFILE PICTURE ----------------- */

    const imgDiv = document.querySelector('.profile-pic');
    const img = document.querySelector('#photo');
    const file = document.querySelector('#profile_file');
    const uploadBtn = document.querySelector('#upload');

    // if user hovers on profile div, then show upload button
    imgDiv.addEventListener('mouseenter', function ()
    {
       uploadBtn.style.display = "block";
    });

    // if we hover out from img div, then hide upload button
    imgDiv.addEventListener('mouseleave', function ()
    {
       uploadBtn.style.display = "none";
    });

    // TODO: Save image in database
    file.addEventListener('change', function()
    {
        const chosenFile = this.files[0];

        if (chosenFile)
        {
            const reader = new FileReader();
            reader.addEventListener('load', function()
            {
                img.setAttribute('src', reader.result)
            });

            reader.readAsDataURL(chosenFile);
        }
    });