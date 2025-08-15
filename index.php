<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Deteksi Komentar</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <div class="container">
    <div class="comment-section">
      <div class="comment-blur">
        <img src="assets/bg.png" alt="blurred" class="blur-image">
      </div>

      <div class="comment-box">
        <p><strong>leslarfamilly</strong> Bismillah 🔥❤️</p>
        <div class="actions">
          <form id="commentForm">
            <input type="text" name="komentar" id="komentar" placeholder="Ketik komentar..." required>
            <button type="submit">Kirim</button>
          </form>
          <div id="hasil"></div>
        </div>
      </div>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
