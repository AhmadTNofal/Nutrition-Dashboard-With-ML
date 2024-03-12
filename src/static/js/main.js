// Wait for the entire document to load before executing the script
document.addEventListener('DOMContentLoaded', function () {
    // Select the mode switch element
    var modeSwitch = document.querySelector('.mode-switch');

    // Initialize dark mode from localStorage
    if (localStorage.getItem('darkMode') === 'true') {
        document.documentElement.classList.add('dark');
        modeSwitch.classList.add('active');
    }

    // Add click event listener to the mode switch to toggle dark mode and active class
    modeSwitch.addEventListener('click', function () { 
        document.documentElement.classList.toggle('dark');
        modeSwitch.classList.toggle('active');

        // Save the dark mode preference in localStorage
        localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
    
    // Select the list view and grid view buttons
    var listView = document.querySelector('.list-view');
    var gridView = document.querySelector('.grid-view');
    
    // Select the container that holds the projects
    var projectsList = document.querySelector('.project-boxes');
    
    // Add click event to switch to list view, remove grid view class and add list view class
    listView.addEventListener('click', function () {
        gridView.classList.remove('active');
        listView.classList.add('active');
        projectsList.classList.remove('jsGridView');
        projectsList.classList.add('jsListView');
    });
    
    // Add click event to switch to grid view, remove list view class and add grid view class
    gridView.addEventListener('click', function () {
        gridView.classList.add('active');
        listView.classList.remove('active');
        projectsList.classList.remove('jsListView');
        projectsList.classList.add('jsGridView');
    });

    // Add click event to show messages section
    document.querySelector('.messages-btn').addEventListener('click', function () {
        document.querySelector('.messages-section').classList.add('show');
    });

    // Add click event to close messages section
    document.querySelector('.messages-close').addEventListener('click', function() {
        document.querySelector('.messages-section').classList.remove('show');
    });
});

// Select elements related to the file upload area
const dropArea = document.querySelector(".drop_box"),
    button = dropArea.querySelector("button"),
    dragText = dropArea.querySelector("header"),
    input = dropArea.querySelector("input");
let file; // Variable to store the selected file
var filename;

// Trigger file input click when button is clicked
button.onclick = () => {
    input.click();
};

// Handle file selection
input.addEventListener("change", function (e) {
    var fileName = e.target.files[0].name; // Get the name of the selected file
    // Create form to display the selected file name and an upload button
    let filedata = `
        <form action="{{ url_for('upload') }}" method="post">
        <div class="form">
        <h4>${fileName}</h4>
        <button class="btn">Upload</button>
        </div>
        </form>`;
    // Update the drop area with the form
    dropArea.innerHTML = filedata;
});

function updateLowerValue(val) {
    var lowerLabel = document.getElementById('lower-label');
    lowerLabel.innerHTML = val + '%';
    
    // Ensure the lower slider does not cross over the upper slider
    var upperVal = parseInt(document.getElementById('upper').value);
    if (parseInt(val) > upperVal) {
        document.getElementById('lower').value = upperVal;
        lowerLabel.innerHTML = upperVal + '%';
    }
}

function updateUpperValue(val) {
    var upperLabel = document.getElementById('upper-label');
    upperLabel.innerHTML = val + '%';
    
    // Ensure the upper slider does not cross under the lower slider
    var lowerVal = parseInt(document.getElementById('lower').value);
    if (parseInt(val) < lowerVal) {
        document.getElementById('upper').value = lowerVal;
        upperLabel.innerHTML = lowerVal + '%';
    }
}

function updateVisualTrack() {
    var lowerVal = parseInt(document.getElementById('lower').value, 10);
    var upperVal = parseInt(document.getElementById('upper').value, 10);
    var maxVal = parseInt(document.getElementById('lower').max, 10);

    var percentageLower = (lowerVal / maxVal) * 100;
    var percentageUpper = (upperVal / maxVal) * 100;

    var slider = document.querySelector('.multi-range-slider');
    slider.style.setProperty('--range-width', `${percentageUpper - percentageLower}%`);
    slider.style.setProperty('--range-start', `${percentageLower}%`);
}

  // Initialize visual track
updateVisualTrack();

  // Add event listeners
document.getElementById('lower').addEventListener('input', function() {
    updateLowerValue(this.value);
    updateVisualTrack();
});
document.getElementById('upper').addEventListener('input', function() {
    updateUpperValue(this.value);
    updateVisualTrack();
});
