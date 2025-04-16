$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$mensaje = "Respaldo automático: $fecha"

git add .
git commit -m "$mensaje"
git push
