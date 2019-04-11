function btn_close(){
	let div = document.getElementsByClassName('bg-modal')
	for(let i = 0; i < div.length; i++)
		div[i].style.display = 'none'
}

function ver_docente(id){
	let div = document.getElementById('docente' + id.toString())
	div.style.display = 'flex'
}

function ver_aluno(id){
	let div = document.getElementById('aluno' + id.toString())
	div.style.display = 'flex'	
}

function vincular_docente(){
	let div = document.getElementById('vincular-docente')
	div.style.display = 'flex'
}