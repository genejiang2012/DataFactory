/*
 * @Author: gene.jiang
 * @Date: 2023-05-15 17:50:13
 * @LastEditors: gene.jiang
 * @LastEditTime: 2023-05-15 19:42:17
 * @Description: file content
 * @FilePath: \DataFactory\index.js
 */
const faker = require('./faker.js');

for (let i = 0; i <10; i++){
    const firstName = faker.name.firstName()
    const lastName = faker.name.lastName()
    const suffix = faker.name.suffix()
    const jobTitle = faker.name.jobTitle()

    console.log(`${suffix} ${firstName} ${lastName} works as '${jobTitle}'`)
}

const randomName= faker.internet.email()
const randomCard = faker.helpers.createCard()
console.log(`${randomName} is '${randomCard.name}'`)

const User = {
    name: faker.name.findName(),
    email: faker.internet.email(),
    website: faker.internet.url(),
    address: faker.address.streetAddress() + faker.address.city() + faker.address.country(),
    bio: faker.lorem.sentences(),
    image: faker.image.avatar(),
}

console.log(`${User}`)

// const faker = require ( 'faker' );
  let database = { users : []};
  const threshold = 2 ;
 
  for ( let i = 1 ; i<= threshold; i++) {
  database.users.push({
    id : i,
    name : faker.name.firstName() + " " + faker.name.lastName(),
    job : faker.name.jobTitle(),
    about : faker.lorem.paragraph(),
    phone : faker.phone.phoneNumber(),
    userName : faker.internet.userName(),
    email : faker.internet.email(),
    salary : "$" + faker.finance.amount() + "M" ,
    // You can also use faker.image.people() for image
    image: "https://source.unsplash.com/1600x900/?user" , 
    country : faker.address.country()
  });
 }
 
  console .log(JSON .stringify(database));
