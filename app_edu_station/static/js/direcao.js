function verificar_senha(){
	let btn = document.getElementsByName('submit')[0]
	if(document.getElementsByTagName('password').value === document.getElementsByTagName('password').value)
		btn.disabled = true
	else
		btn.disabled = false

}