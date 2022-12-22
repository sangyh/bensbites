<template>
    <p class="px-10"> Just browsing? Here are trending topics on Ben's Bites:</p>
    <div class="trending-topics-container">
        <div v-for="topic in topics" :key="topic" class="trending-topic">
            <button @click="emitResult">{{ topic }}</button>
        </div>
    </div>
</template>

<script>

export default {
    props:['topics'],
    emits: ["selectedtopic"],

    methods: {
        emitResult(event) {
            this.$emit('selectedtopic', event.currentTarget.textContent);
        }
    }

}
</script>

<style>
.trending-topics-container {
  padding: 0 1rem;
  font-size: 1.5rem;
  max-height: 128px;
  display: flex; /* this will make the trending topics display in a row */
  flex-wrap: wrap; /* this will allow the trending topics to wrap onto multiple lines if necessary */
  overflow-x: auto; /* this will add a horizontal scrollbar if the trending topics don't fit on a single line */
  justify-content: center;
}

.trending-topic {
  background-color: #e53e3e;
  color: #fff;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.2rem .2rem;
  border-radius: 0.25rem;
  display: inline-block;
  margin-right: .2rem;
  margin-bottom: .2rem;
  width: auto;
}


.trending-topic:hover {
  background-color: #c53030;
}

</style>
