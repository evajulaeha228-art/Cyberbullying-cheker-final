<?php
$komentar = $_POST['komentar'];

$data = array("komentar" => $komentar);
$options = array(
    'http' => array(
        'header'  => "Content-type: application/json\r\n",
        'method'  => 'POST',
        'content' => json_encode($data),
    ),
);

$context  = stream_context_create($options);
$response = file_get_contents('http://localhost:5000/klasifikasi', false, $context);

if ($response === FALSE) {
    echo '<span style="color:gray;">⚠️ Gagal menghubungi server klasifikasi.</span>';
    exit;
}

$result = json_decode($response, true);
$label = $result['label'];

if ($label == 'Cyberbullying') {
    echo '<span style="color:red;">❌ Komentar mengandung Cyberbullying</span>';
} else {
    echo '<span style="color:green;">✅ Komentar Bukan Cyberbullying</span>';
}
?>
