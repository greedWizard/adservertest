<template>
  <div>
    <div class="ad-info">
      <header-info> </header-info>
      <h3>Новое объявление</h3>
      <p>* - обязательные поля</p>
      * <a>Название объявления: <input placeholder="Я продаю.." v-model="title"></a> <br>
      * <a>Цена: <input v-model="price" placeholder="Цена товара"> </a> <br>
      * <a>Описание: <textarea placeholder="Вы должны это купить потому что.." v-model="desc"> </textarea></a><br> <br>
      * <a> Категория:
        <select v-model="newCategory" @change="writeFields"> 
          <option selected disabled>Категория</option>
          <option v-for="category in this.categories" v-bind:value="category.id" v-bind:key="category" :disabled="category.children.length > 0">
            {{ category.name }}
          </option>
        </select>
      </a>
      <a><h4>Фото товара</h4></a>
      <span>Загружайте фото товара, чтобы показать его товарный вид.</span>
      <input type="file" id="product_images" @change="uploadImages" accept="image/" multiple>
    </div>
    <div> 
      <h4>Дополнительно о товаре</h4>
      <a v-for="field in this.necessaryFields" v-bind:key="field"> * {{ field.name }}: <input v-bind:type="field.type" v-bind:placeholder="field.name" v-bind:id="field.name">  <br></a>
    </div>
    <hr>
    <div class="adress-info"> 
      <a> <h3>Вы находитесь</h3> </a>
      <a>
        * <select v-model="newState" @change="loadCities">
         <option disabled selected>Выберите область</option>
         <option v-for="state in this.states" v-bind:key="state" v-bind:value="state.id" >
           {{ state.name }}
         </option>
       </select>
       * <select v-model="newCity" @change="loadRegions">
         <option selected disabled>Город</option>
         <option v-for="city in this.cities" v-bind:key="city" v-bind:value="city.id">{{ city.name }}</option>
       </select>
       * <select v-model="newRegion">
         <option disabled selected>Район</option>
         <option v-for="region in this.regions" v-bind:key="region" v-bind:value="region.id"> {{ region.name }} </option>
       </select> <br> <br>
       <a>Улица: <input v-model="street" placeholder="Улица"> </a>
       <a>Дом: <input v-model="house" placeholder="Номер дома"></a>
      </a>
    </div>
    <br<br>
    <button @click="sendAd">Отправить</button>

  </div>
</template>

<script>
import Header from '../Header'
import User from '../../mixins/User'
import AdsUtils from '../../mixins/AdsUtils'

import $ from 'jquery'

export default {
  name: 'CreateAds',
  data(){
    return {
      productImages: [],
      newState: 'Область',
      newRegion: 'Район',
      newCity: 'Город',
      cities: [],
      desc: '',
      title: '',
      countries: undefined,
      states: undefined,
      regions: undefined,
      cities: undefined,
      categories: [],
      newCategory: 'Категория',
      street: '',
      house: '',
      newCategoryInfo: '',
      necessaryFields: [],
      newFields: [],
    }
  },
  created()
  {
      this.loadUser();
      this.loadStates();
      this.loadCategories();
  },
  components: {
      'header-info': Header,
  },
  methods: {
    uploadImages(e)
    {
      this.productImages = e.target.files;
    },
    writeFields(e)
    {
      $.ajax({
        url: 'http://localhost:8000/api/board/categories/' + this.newCategory,
        type: 'GET',
        success: (response) => {
          this.necessaryFields = response.data.info.necessary_fields;
        },
        error: (response) => {
          alert('Не удалось получить дополнительные поля');
        }
      });
    },
    loadStates()
    {
      $.ajax({
        url: 'http://localhost:8000/api/locations/states/?country_id=1',
        type: 'GET',
        success: (response) => {
          this.states = response.data.info;
          this.regions = [];
        },
        error: (response) => {
          
        }
      });
    },
    loadCities()
    {
      $.ajax({
        url: 'http://localhost:8000/api/locations/cities/?state_id=' + this.newState,
        type: 'GET',
        success: (response) => {
          this.cities = response.data.info;
        },
        error: (response) => {
          
        }
      });
    },
    loadRegions()
    {
      $.ajax({
        url: 'http://localhost:8000/api/locations/regions/?city_id=' + this.newCity,
        type: 'GET',
        success: (response) => {
          this.regions = response.data.info;
        },
        error: (response) => {

        }
      });
    },
    loadCategories()
    {
      $.ajax({
        url: 'http://localhost:8000/api/board/categories/',
        type: 'GET',
        success: (response) => {
          this.categories = response.data.info;
        },
        error: (response) => {
          console.error(response);
        }
      })
    },
    sendAd()
    {
      if(!this.newCity || !this.newRegion || !this.desc || !this.price || !this.title ||
      !this.newCategory) {
        // сообщения об обязательном поле тут (вставлю потом)
        return;
      }

      var formData = new FormData();
      
      for(var i = 0; i < this.productImages.length; i++)
      {
        formData.append('imgs', this.productImages[i], this.productImages[i].name)
      }

      var necessary_fields = {};

      console.log(this.necessaryFields);

      for(var i=0; i < this.necessaryFields.length; i++) {
        var val = document.getElementById(this.necessaryFields[i].name).value;
        necessary_fields[this.necessaryFields[i].name] = val;
      }

      formData.append('title', this.title);
      formData.append('price', this.price);
      formData.append('desc', this.desc);
      formData.append('category', this.newCategory);
      formData.append('state', this.newState);
      formData.append('city', this.newCity);
      formData.append('region', this.newRegion);

      if(this.street) {
        formData.append('street', this.street);
      }
      if(this.house) {
        formData.append('house', this.house);
      }

      formData.append('data', JSON.stringify(necessary_fields));

      $.ajax({
        url: 'http://localhost:8000/api/board/ads/',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: (response) => {
          console.log(response);

          if(!response.data.errors){
            this.$router.push({name: 'adDetails', params: {ad_id: response.data.created_ad }})
          }
        },
        error: (response) => {
          console.log(response);
          alert('ошибка');
        }
      });
    }
  },

  mixins: [
      User,
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
