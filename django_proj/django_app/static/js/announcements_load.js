    function funonload() {
        var refreshForm = document.createElement("form");
        refreshInput.method = "POST";
        refreshInput.action = "announcements";
        refreshInput.hidden = "hidden";

        var refreshInput = document.createElement("input");
        refreshInput.type = "hidden";
        refreshInput.name = "refresh";
        refreshInput.value = 1;
        refreshForm.appendChild(refreshInput);

        refreshForm.submit();
    }
    window.onload = funonload;