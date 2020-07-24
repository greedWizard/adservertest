import $ from 'jquery'


export default {
    data()
    {
        return {
            ads: [],
        }
    },
    methods: {
        getAds() {
            $.ajax({
                async: false,
                url: 'http://localhost:8000/api/board/ads/',
                type: 'GET',
                success: (response) => {
                    this.ads = response.data.info;
                },
                error: (response) => {
                    console.error("Couldn't get ads");
                    console.log(response);
                }
            })
        }
    }
}