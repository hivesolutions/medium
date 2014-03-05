<div class="error">
    <img src="${out value=base_path /}resources/images/broken-transmission.png" />
    <p class="title">Something went terribly wrong</p>
    <p class="message">${out value=exception_message xml_escape=True /}</p>
</div>
