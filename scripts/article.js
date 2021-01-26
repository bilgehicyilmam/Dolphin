let data = [{ "exact": "hasan" }, { "exact": "ali" }, { "exact": "hasan" }]

function isBigEnough(value) {
    console.log(value)

    return value.exact
}


let filtered = data.filter(isBigEnough)
// filtered is [12, 130, 44]

console.log(filtered)

const names = [
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "alie" } } },
];

let new_names = []

names.forEach(
    (element) => {
        console.log(element)
        
        new_names.push(element)
    } 
    );


console.log(new_names)

let x = (names) => names.filter(function (v, i) {

    let exact = v.target.selector.exact
    console.log(exact, i)
    console.log(names[i].target.selector.exact === exact)
    console.log(names[i].target.selector.exact === i)
    return names[i].target.selector.exact === i
    //    return  names.indexOf(v) === i
})

new_list = x(names); // 'John', 'Paul', 'George', 'Ringo'

console.log(new_list)


let products= [
    {
      id: 01,
      items: [
        {
          id: 01,
          name: 'apple'
        },
        {
          id: 02,
          name: 'banana'
        },
        {
          id: 03,
          name: 'orange'
        }
      ]
    },
    {
      id: 02,
      items: [
        {
          id: 01,
          name: 'carrot'
        },
        {
          id: 02,
          name: 'lettuce'
        },
        {
          id: 03,
          name: 'peas'
        }
      ]
    },
    {
      id: 03,
      items: [
        {
          id: 01,
          name: 'eggs'
        },
        {
          id: 02,
          name: 'bread'
        },
        {
          id: 03,
          name: 'milk'
        }
      ]
    }
  ]


 let hasan = products.find((product) => {
    return product.items.some((item) => {
  //^^^^^^
      return item.name === 'milk';
    });
  });

  console.log(hasan)

  const annotations = [
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "hasan" } } },
    { 'target': { 'selector': { 'exact': "alie" } } },
];


let hasan = annotations.find((annotation) => {
    return annotation.target.selector.some((item) => {
  //^^^^^^
      return item.name === 'hasan';
    });
  });
