// connects to about


const getFormData = async (e) => {
    e.preventDefault();
    const pokemon = e.target.pokemon.value;
    const url = `https://pokeapi.co/api/v2/pokemon/${pokemon}`;


    const res = await fetch(url);
    // console.log('res', res)

    const data = await res.json();
    // console.log('data', data)


    const name = data['name'];
    const id = data.id;
    const imgUrl = data.sprites.other["official-artwork"].front_default
    const baseHp = data.stats[0].base_stat
    const baseAtt = data.stats[1].base_stat
    const baseDef = data.stats[2].base_stat
    const ability1 = data.abilities[0].ability.name
    const ability2 = data.abilities[1].ability.name



    console.log(name,id, imgUrl)



    const myData = {
        name: name,
        id: id,
        imgUrl : imgUrl,
        baseHp : baseHp,
        baseAtt : baseAtt,
        baseDef : baseDef,
        ability1 : ability1,
        ability2 : ability2,
        

    }

  addToPage(myData)
};

//
// const myForm= document.getElementById('myForm')
// myForm.addEventListener('submit', getFormData)


const addToPage =(p) => {
  const card = document.createElement('div');
  // card.classList.add('my-4');
  card.innerHTML = `
  <div class="card text-center" style="width: 18rem;">
    <img src="${p.imgUrl}" class="card-img-top" alt="${p.name}">
    <div class="card-body">
      <h5 class="card-title" >
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
  </svg>
    ${p.name}
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
  </svg>
  </h5>
    
    <p class="card-text">HP: ${p.baseHp}</p>
    <p class="card-text">Attack: ${p.baseAtt}</p>
    <p class="card-text">Defense: ${p.baseDef}</p>
    <p class="card-text">Ability: ${p.ability1}</p>
    <p class="card-text">Ability: ${p.ability2}</p>
   
  </div>
</div>
  `

  const container = document.querySelector('.container');
  if (container.innerHTML !== ''){
      container.innerHTML = ''
  }
  container.append(card)

};


const myForm = document.getElementById('myForm');
myForm.addEventListener('submit', getFormData)
