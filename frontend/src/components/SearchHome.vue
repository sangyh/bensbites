<template>
    <!-- Jumbotron -->
    <div class="relative bg-gray-50 w-full text-center"> 
        <div class="flex items-center justify-center py-10">
            <img
            src="~@/assets/bensbites_logo.jpg"
            alt="Bens bites logo"
            />
        </div>
        <div class="mx-16">
            <h1 class="text-3xl font-bold mt-0 mb-6">Ben's Bites Lookup</h1>
            <h3 class="text-1xl font-bold mb-8"> Semantic search to help find your favorite AI tools</h3>
            <a href="https://twitter.com/sangyh2" class="text-gray-700 mb-8 leading-relaxed text-l">
                Built by @sangyh2
            </a>
        </div>
    </div>
    <!-- Jumbotron -->

    <form @submit.prevent="search" class="flex justify-center items-center py-10">
      <input type="text" v-model="query" placeholder="Search..." class="w-2/5 py-2 px-3 rounded-md bg-gray-200 placeholder-gray-700"/>
      <button type="submit"  class="py-2 px-3 rounded-md bg-blue-500 text-white">Go</button>
    </form>
    
    <!-- <div class="bg-gray-100" v-if="results.length > 0">
      <ul>
        <li v-for="result in results" :key="result.id">
          {{ result.url}},  {{result.text}},  {{result.extlink}}
        </li>
      </ul>
    </div> -->
    <div v-if="isLoading" class="bg-gray-200 h-12 w-12 rounded-full">
      <p>LOADING</p>
    </div>
    
    <div v-else>
      <div class="bg-gray-100 mx-auto mt-5 px-4 py-4" v-if="results.length > 0">
        <div class="flex justify-between items-center mb-4 font-semibold text-gray-800">
            <div class="w-1/5">Blog</div>
            <div class="w-1/5">Category</div>
            <div class="w-1/5">Tool</div>
            <div class="w-1/5">Link</div>
            <div class="w-1/5">Similarity</div>
        </div>

        <table class="table-fixed w-full">
          <tbody>
            <tr v-for="row in results" :key="row">
              <td v-for="value in row" v-bind:key="value"  class="justify-between items-center mb-4 w-1/5">{{ value }}</td>
            </tr>
          </tbody>
        </table> 
        

      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      results: [],
      isLoading: false,
      hasError: false
    }
  },
  methods: {
    async search() {
      this.isLoading = true;
      try {
        // process response data
        const response = await axios.get('/search/semanticsearch/', {
        params: {
          q: this.query
        }
      });
      this.results = JSON.parse(response.data);
      } catch (error) {
        // Display an error message to the user
        this.errorMessage = 'There was an error while fetching the data';

        // Log the error
        console.error(error);

        // Update the UI to reflect the error state
        this.hasError = true;
      } finally {
        this.isLoading = false;
      }
    }
  }
}

</script>

