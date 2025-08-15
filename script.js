document.getElementById('commentForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const komentar = document.getElementById('komentar').value;

  fetch('classify.php', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'komentar=' + encodeURIComponent(komentar)
  })
  .then(response => response.text())
  .then(data => {
    document.getElementById('hasil').innerHTML = data;
  });
});
