function mascara_cpf(){
	let cpf = document.getElementsByClassName('cpf')

	for(let i = 0; i < cpf.length; i++){
		let text = cpf[i].innerText
		let cpf_mascarado = ''

		cpf_mascarado += text[0] + text[1] + text[2] + '.'
		cpf_mascarado += text[3] + text[4] + text[5] + '.'
		cpf_mascarado += text[6] + text[7] + text[8] + '-'
		cpf_mascarado += text[9] + text[10]
		
		cpf[i].innerText = cpf_mascarado
	}
}

mascara_cpf()

function pesquisar(){
	let input = document.getElementById('input-pesquisar').value

	let tr = document.getElementsByTagName('tr')
	let tbody = document.getElementsByTagName('tbody')[0]

	let encontrados = []
	for(let i = 0; i < tr.length; i++){

		let nome = tr[i].getElementsByClassName('nome')[0].innerText
		console.log(nome + '  ' + input)
		if(nome === input){
			encontrados.push(tr[i])
		}
	}

	if(encontrados.length > 0){
		tbody.innerText = ''
		for(let i = 0; i < encontrados.length; i++){
			tbody.innerText = tbody.innerText + encontrados[i]
		}
	}

}

function verificar_senha(){
	let btn = document.getElementsByName('submit')[0]
	if(document.getElementsByTagName('password').value === document.getElementsByTagName('password').value)
		btn.disabled = true
	else
		btn.disabled = false

}