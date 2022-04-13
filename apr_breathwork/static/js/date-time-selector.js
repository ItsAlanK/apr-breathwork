 // Fixes Duplicate dates when more than one time available for date//
    // https://stackoverflow.com/questions/22905769/remove-duplicate-options-from-html-select //
    const usedNames = {};
    $("select[name='date'] > option").each(function () {
        if(usedNames[this.text]) {
            $(this).remove();
        } else {
            usedNames[this.text] = this.value;
        }
    });

    // Listens for selected date and shows/hides appropriate times //
    const dateSelector = document.getElementById("date");
    const timeSelector = document.getElementById("time");
    dateSelector.addEventListener("change", function() {
        chosenDate = dateSelector.options[dateSelector.selectedIndex].value;
        for (const i=0; i<timeSelector.length; i++) {
            if (timeSelector.options[i].id == chosenDate) {
                timeSelector.options[i].classList.remove("d-none");
                timeSelector.selectedIndex = null; 
            }
            else {
                timeSelector.options[i].classList.add("d-none");
                timeSelector.selectedIndex = null;
            }
        }
    });