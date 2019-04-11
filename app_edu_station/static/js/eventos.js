function hover_icon(){
    document.getElementById('user-icon').style.cursor = "pointer";
}

function icon_clicked(){
	if (document.getElementById('opcoes-icon').style.display == "block"){
		document.getElementById('opcoes-icon').style.display = "none";	
	}
	else{
		document.getElementById('opcoes-icon').style.display = "block";
	}
}

function mouse_left_icon(){
	document.getElementById('opcoes-icon').style.display = "none";
}

function alterar_senha(){
	document.getElementById('alterar-senha').style.display = "block";
	document.getElementById('alterar-senha-btn').style.display = "none";
}

function gerar_senha(){
	let label = document.getElementById('label-senha')
	label.innerHTML = 'S3NH4NOV4'	
}

function verificar_senha(){
	let btn = document.getElementsByName('submit')[0]
	let password = document.getElementById('password').value
	let conf =  document.getElementById('conf_password').value
	if(password.length >= 8 && conf.length >= 8 && conf === password)
		btn.disabled = false
	else
		btn.disabled = true
}
