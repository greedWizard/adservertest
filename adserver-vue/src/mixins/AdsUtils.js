import $ from 'jquery'

export default {
    data()
    {
        return {
            countries: undefined,
            states: undefined,
            regions: undefined,
            cities: undefined,
            categories: [],
        }
    },
    methods: {
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
        loadStates() {
            $.ajax({
                url: 'http://localhost:8000/api/locations/states/?country_id=1',
                type: 'GET',
                success: (response) => {
                    this.states = response.data.info;
                },
                error: (response) => {
                    console.error('Не удалось загрузить области');
                }
            });
        },
        loadCities(state_id=1) {
            $.ajax({
                url: 'http://localhost:8000/api/locations/cities/?state_id=' + state_id,
                type: 'GET',
                success: (response) => {
                    this.cities = response.data.info;
                },
                error: (response) => {
                    console.log('Не удалось загрузить города')
                }
            });
        },
        loadRegions(city_id=1)
        {
            $.ajax({
                url: 'http://localhost:8000/api/locations/regions/?city_id=' + city_id,
                type: 'GET',
                success: (response) =>
                {
                    this.regions = resopnse.data.regions;
                },
                error: (response) => {
                    console.error('Не удалось загрузить регионы');
                }
            });
        }
    }
}