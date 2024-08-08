<template>
    <div class="image-container">
      <v-stage ref="stage" :config="{ width: imageWidth, height: imageHeight }">
        <v-layer ref="layer">
          <v-image :config="{ image: imageObj, width: imageWidth, height: imageHeight }" />
          <v-rect
            v-for="(result, index) in classificationResults"
            :key="index"
            :config="{
              x: result.x,
              y: result.y,
              width: result.width,
              height: result.height,
              stroke: 'red',
              strokeWidth: 2,
            }"
          />
          <v-text
            v-for="(result, index) in classificationResults"
            :key="index"
            :config="{
              x: result.x,
              y: result.y - 20,
              text: `${result.foodClass} (${(result.confidence * 100).toFixed(2)}%)`,
              fontSize: 14,
              fill: 'white',
              padding: 5,
              fontFamily: 'Calibri',
              align: 'center',
            }"
          />
        </v-layer>
      </v-stage>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue';
  import Konva from 'konva';
  import { createImage } from 'vue-konva';
  
  export default {
    props: {
      imageUrl: String,
      classificationResults: Array,
    },
    setup(props) {
      const stage = ref(null);
      const layer = ref(null);
      const imageObj = ref(null);
      const imageWidth = ref(800);
      const imageHeight = ref(600);
  
      const loadImageAndDraw = () => {
        if (!props.imageUrl) return; // Check if image URL exists
  
        const img = new Image();
        img.src = props.imageUrl;
        img.onload = () => {
          imageObj.value = img;
          imageWidth.value = img.width;
          imageHeight.value = img.height;
  
          if (props.classificationResults) {
            drawBoundingBoxes(props.classificationResults);
          }
        };
      };
  
      const drawBoundingBoxes = (results) => {
        layer.value.destroyChildren(); // Clear previous boxes
  
        results.forEach(result => {
          // Create bounding box (v-rect)
          // Create label (v-text)
          // Add both to layer.value
        });
      };
  
      onMounted(loadImageAndDraw);
      watch(() => props.classificationResults, drawBoundingBoxes);
      watch(() => props.imageUrl, loadImageAndDraw); 
  
      return {
        stage,
        layer,
        imageObj,
        imageWidth,
        imageHeight,
      };
    },
  };
  </script>
  