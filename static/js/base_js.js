document.getElementById('closeButton').onclick = function() {
    document.getElementById('errorContainer').style.display = 'none';
}

function updateFileName() {
    const input = document.getElementById('id_photo');
    const fileNameDisplay = document.getElementById('file-name');

    if (input.files.length > 0) {
        fileNameDisplay.textContent = input.files[0].name;
    } else {
        fileNameDisplay.textContent = 'Нет файла';
    }
}