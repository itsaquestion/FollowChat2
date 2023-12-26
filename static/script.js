// Function to apply formatting to text
function applyFormatting(text) {
  // Replace newlines with <br> tags
  text = text.replace(/\n/g, '<br>');

  // Make text between [] strong, while keeping the brackets
  return text.replace(/\[(.*?)\]/g, '<strong><span style="font-family:sans-serif;">[$1]</span></strong>');
}

// Fetch the list of files when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  fetch('/list_files')
    .then(response => response.json())
    .then(data => {
      data.sort().reverse();
      const fileList = document.getElementById('fileList');
      data.forEach(fileName => {
        const displayName = fileName.replace('.txt', '').replace(/_News_/g, ': ').replace(/_/g,'');

        const listItem = document.createElement('li');
        listItem.textContent = displayName;

        // Add click event to each file list item
        listItem.addEventListener('click', function () {
          
          // Remove 'selected-file' class from all list items
          const allListItems = fileList.getElementsByTagName('li');
          for (let i = 0; i < allListItems.length; i++) {
            allListItems[i].classList.remove('selected-file');
          }

          // Add 'selected-file' class to the clicked list item
          this.classList.add('selected-file');

          fetch('/read_file', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ file_name: fileName })
          })
            .then(response => response.json())
            .then(content => {
              const formattedContent = applyFormatting(content);
              document.getElementById('fileContent').innerHTML = formattedContent;
            });
        });

        fileList.appendChild(listItem);
      });
    });
});
