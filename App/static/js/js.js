function deleteNote(noteId) {
    fetch('/index', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ noteId: noteId })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log(data.message); // or handle success as needed
        window.location.href = "/";
    })
    .catch(error => {
        console.error('There was an error!', error);
        // Handle error
    });