<template>
  <div>
    <div class="bg-gray-100 mx-auto mt-5 px-4 py-4" v-if="results.length > 0">
      <div class="flex flex-col">
        <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="py-2 inline-block min-w-full sm:px-6 lg:px-8">
            <div class="overflow-x-auto">
              <table class="table-fixed min-w-full border-t border-b">
                <thead class="border-b">
                  <tr>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Post
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Section
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Info
                    </th>
                    <th scope="col" class="text-sm font-medium text-gray-900 px-6 py-4 text-left">
                      Link
                    </th>
                    
                  </tr>
                </thead>


                <tbody>
                  <tr v-for="row in results" :key="row" class="overflow-x-auto border-b">
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
                  </tr>
                </tbody>
              </table> 
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>

export default {
  props: ['results'],

  methods: {
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

