<template>
    <head>
      <link rel="icon" type="image/x-icon" href="/favicon.ico">
      <title>BensBites Tracker</title>
    </head>
    <!-- Jumbotron -->
    <div class="relative bg-gray-50 w-full text-center mb-4"> 
        <div class="flex items-center justify-center py-5">
            <img
            src="~@/assets/bensbites_logo.jpg"
            alt="Bens bites logo"
            />
        </div>
        <div class="mx-16">
            <h1 class="text-3xl font-bold mt-0 mb-2">Ben's Bites Tracker</h1>
            <h3 class="text-1xl font-bold mb-0.5"> Find your favorite AI tools from <a class="text-red-500" href="https://bensbites.beehiiv.com/" target="_blank">Ben's Bites</a></h3>
            <p class="text-gray-700 leading-relaxed text-l ">
                Built by 
                  <a href="https://twitter.com/sangyh2" class="text-blue-500 underline">@sangyh2</a>
            </p>
        </div>
    </div>
    <!-- Jumbotron -->

    <form @submit.prevent="search" class="flex justify-center items-center py-2">
      <input type="text" v-model="query" placeholder="Search..." class="w-2/5 py-2 px-3 rounded-md bg-gray-200 placeholder-gray-700"/>
      <button type="submit"  class="py-2 px-3 rounded-md bg-blue-500 text-white">Go</button>
    </form>
    <div class="'w-full text-center px-5 py-5'">
      <p> Try searching for "stable diffusion" or "podcasting AI tools"</p>
    </div>

    <!-- Load all topics -->
    <div>
      <allTopics v-bind:topics="topics" @selectedtopic="filterTopics"/>
    </div>
    
    
    <div v-if="isLoading" class="w-full text-center px-20 py-4">
      <p class="">Hang tight...</p>
    </div>
    
    <div v-else>
      <SearchResults v-bind:results="results"/>
    </div>
</template>

<script>
import axios from 'axios';
import SearchResults from './SearchResults'
import allTopics from './allTopics'

export default {
  components: {
    SearchResults,
    allTopics
  },

  data() {
    return {
      query: '',
      results: [],
      topics:[],
      topic2filter:'',
      isLoading: false,
      hasError: false
    }
  },

  mounted: function() {
    this.search(),
    this.get_topics()
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
      console.log(this.results)

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
    },
    
    async get_topics() {
      try {
        // process response data
        const response = await axios.get('/search/topics/');
        this.topics = response.data;
      } catch (error) {
        // Display an error message to the user
        this.errorMessage = 'There was an error while fetching the data';

        // Log the error
        console.error(error);

        // Update the UI to reflect the error state
        this.hasError = true;
      } 
    },

    async filterTopics(selectedtopic){
      this.isLoading = true;
      /* endpoint: filtertopics */
      try {
        // process response data
        const response = await axios.get('/search/filtertopics/', {
        params: {
          q: selectedtopic
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
  },
}

</script>

<style>
  /* Add the overflow-x-auto class to the table row */
  tr.overflow-x-auto {
    /* Use the 'table-row' display value to ensure that the table row maintains its normal layout */
    display: table-row;
    /* Apply the horizontal scrolling */
    overflow-x: auto;
  }
</style>