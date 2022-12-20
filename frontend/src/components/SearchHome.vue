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
    
    
    <div v-if="isLoading" class="w-full text-center px-20 py-4">
      <p class="">Hang tight...</p>
    </div>
    
    <div v-else>
      <div class="bg-gray-100 mx-auto mt-5 px-4 py-4" v-if="results.length > 0">
        <div class="flex justify-between items-center mb-4 font-semibold text-gray-800">
            <div class="w-4/12">Post</div>
            <div class="w-2/12">Section</div>
            <div class="w-4/12">Info</div>
            <div class="w-1/12">Link</div>
            <div class="w-1/12">Similarity</div>
        </div>

        <table class="table-fixed w-full border-t border-b">
          <tbody>
            <tr v-for="row in results" :key="row" class="overflow-x-auto">
              <!-- <td v-for="value in row" v-bind:key="value"  class="justify-between items-center mb-4 w-1/5">{{ value }}</td> -->
              <td class="border-t justify-between items-center mb-4 w-4/12 px-1 text-blue-500 underline">
                <a v-bind:href="row.url" target="_blank">{{ row.url }}</a>
              </td>
              <td class="border-t justify-between items-center mb-4 w-2/12 px-1">{{ row.section }}</td>
              <td class="border-t justify-between items-center mb-4 w-4/12 px-1">{{ row.item_text }}</td>
              <td class="border-t justify-between items-center mb-4 w-1/12 px-1">
                <ul>
                  <li  v-for="ext_url in row.item_url" :key="ext_url">
                     <p class="text-blue-500 underline" v-html=formattedSentence(ext_url)></p>
                  </li>
                </ul>
              </td>
              <td class="border-t justify-between items-center mb-4 w-1/12 px-1">{{ row.similarity }}</td>
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
    },

    formattedSentence(row) {
      const text = 'link' /* row[0] */
      const url = row[1]
      const newtext = `<a href="${url}" target="_blank">${text}</a>`;
      return newtext
      /* const sentence = row.item_text
      console.log('inside computed:', row)
      
      const newtext = `<a href="${url}">${text}</a>`;
      const formattedsent = sentence.replace(text, newtext); 
      console.log(formattedsent)
      return formattedsent */
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