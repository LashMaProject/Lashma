<template>
    <div>
        <input type="file" @change="onFileChange" accept="image/*"  aria-label="File input"/>
        <img v-if="previewUrl" :src="previewUrl" alt="Preview">
        <button @click="uploadImage" :disabled="!selectedFile">Upload</button>
        <p v-if="loading">Uploading...</p>
        <p v-if="error">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            selectedFile: null,
            previewUrl: null,
            loading: false,
            error: null
        };
    },
    methods: {
        handleFileChange(event) {
            this.selectedFile = event.target.files[0];
            this.previewUrl = URL.createObjectURL(this.selectedFile);
        },
        uploadImage() {
            this.loading = true;
            this.error = null;

            const formData = new FormData();
            formData.append('image', this.selectedFile);

            axios.post('/classify', formData)
                .then(response => {
                    // Handle response
                    this.loading = false;
                })
                .catch(error => {
                    // Handle error
                    this.loading = false;
                    this.error = 'An error occurred while uploading the image.';
                });
        }
    }
};
</script>

<!-- 
<template>
    <div class="image-upload-container">
    <input type="file" ref="fileInput" accept="image/*" @change="onFileChange" aria-label="File input">
      <button @click="uploadImage" :disabled="!selectedFile">Upload Image</button>
  
      <div v-if="selectedFile" class="image-preview">
        <img :src="imagePreviewUrl" alt="Selected Image">
      </div>
    </div>
  </template>
  <script>
   -->