<template>
  <div>
    <header-info> </header-info>
    <h3>Найти подходящее объявление</h3>
    <form @submit="showResults">
      <div id="budget">Бюджет: <br> 
        Крайняя цена: <input v-model="maxPrice" type="range" step="100" v-bin:min="minPrice" max="2000000">
        <input v-model="maxPrice" type="number" step="100" v-bind:min="minPrice" max="2000000"> <br>
        Желаемая цена: <input v-model="minPrice" type="range" step="100" v-bind:max="maxPrice" min="0">
        <input type="number" v-model="minPrice" step="100" min="100">
      </div><br>
      <div> 
        Категория:
        <select v-model="searchCategory" @change="writeFields(searchCategory)"> 
          <option selected disabled >Категория</option>
          <option v-for="category in this.categories" v-bind:value="category.id" v-bind:key="category" :disabled="category.children.length > 0">
            {{ category.name }}
          </option>
        </select>
      </div>
      <div> 
        <h4>Детали</h4>
        <a v-for="field in this.necessaryFields" v-bind:key="field"> {{ field.name }}: <input v-bind:type="field.type" v-bind:placeholder="field.name" v-bind:id="field.name" min="0">  <br></a>
      </div>
      <div> 
        <h4>Искать в</h4>
        {{ searchState }}
        <select v-model="searchState" multiple> 
          <option selected disabled>Область</option>
          <option v-for="state in states" v-bind:key="state" v-bind:value="state.id">{{ state.name }}</option>  
        </select>
      </div>
      <input type="submit" value="Найти"> 
    </form>
    <ads :ads="this.searchAds"> </ads>
  </div>
</template>

<script>
import AdLoader from "../../mixins/AdLoader";
import User from '../../mixins/User'
import Header from '../Header'
import AdsUtils from '../../mixins/AdsUtils'
import Ads from '../board/Ads'

import $ from 'jquery'

export default {
  name: 'Search',
  data() {
    return {
      minPrice: 500,
      maxPrice: 100000,
      categories: [],
      searchCategory: 'Категория',
      searchState: 'Область',
      necessaryFields: [],
      regions: [],
      states: [],
      searchAds: [],
    }
  },
  mixins: [
      User,
      AdsUtils,
  ],
  created()
  {
    this.loadUser();
    this.loadCategories();
    this.loadStates();
    this.showResults();
  },
  methods: {
    showResults() {
      if(Object.keys(this.$route.query).length === 0) {
        
      }
      else {
        $.ajax({
          url: 'http://localhost:8000/api/board/ads/',
          type: 'GET',
          data: this.$route.query,
          success: (response) => {
            this.searchAds = response.data.info;
          },
        });
      }
    },
    writeFields(category_id) {
      $.ajax({
        url: 'http://localhost:8000/api/board/categories/' + category_id,
        type: 'GET',
        success: (response) => {
          this.necessaryFields = response.data.info.necessary_fields;
        },
        error: (response) => {
          alert(error);
        }
      });
    },
    loadStates() {
      $.ajax({
        url: 'http://localhost:8000/api/locations/states/?country_id=1',
        type: 'GET',
        success: (response) => {
          this.states = response.data.info;
        },
        error: (response) => {
          console.log(response);
        }
      });
    }
  },
  components: {
      'header-info': Header,
      'ads': Ads,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>