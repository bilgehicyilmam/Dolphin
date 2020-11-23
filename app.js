// import ontologies from './ontologies.js'
// import articles from './articles.js'

class Reader {
  constructor () {
    console.log('# Constructor')
  }

  addEventListener (className) {
    console.log(`# Set Event Listener to ${className}`)
    const divs = document.querySelectorAll(className)
    console.log(divs)
    divs.forEach(el => el.addEventListener('click', event => {
      let id = event.target.id
      console.log('## ' + id)
      // handle with click event
      this.handleClick(id)

    }))
  }

  handleClick (id) {
    let jsonld = document.getElementById('jsonld').text
    jsonld = JSON.parse(jsonld)
    let value =jsonld.body.value;
    console.log('#jsonld :' + jsonld)
    console.log('##value ' + value)
    alert(value)
  }

  handleId () {}
  getToolTip () { }
}

