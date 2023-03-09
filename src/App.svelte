<script lang='ts'>
  import { createWorker } from 'tesseract.js';
  import { parseLanguagesCSV } from './ts/languages';
  import './styles/app.css';

  import type { Language } from './ts/languages';
  
  let inputFiles: FileList;

  // Load language from static route
  async function loadLanguages(): Promise<Language[]> {
    const language_data = await fetch('/static/languages.csv')
      .then((response) => response.text())
      .then((data) => data);

    return await parseLanguagesCSV(language_data);
  }

  // Preview image after upload
  async function previewImage(blob: Blob) {
    const url: string = URL.createObjectURL(blob);
    const selectionElement = document.getElementById('language-selector') as HTMLInputElement;
    const previewImage: HTMLImageElement = document.getElementById('preview-image') as HTMLImageElement;

    previewImage.src = url;
    await extractText(blob, selectionElement.value);
  }

  // Check if input file is a valid image
  async function validateInputFile() {
    const inputFile = inputFiles[0];
    const acceptedFormats = ['image/png', 'image/jpeg'];

    if (!inputFile) return;

    for (const format of acceptedFormats) {
      if (inputFile.type === format) {
        const blob = new Blob([inputFile], { type: format });
        previewImage(blob);
      }
    }
  }

  // Extract text from image
  async function extractText(blob: Blob, language: string) {
    const worker = await createWorker({
      logger: (m) => console.log(m)
    });

    await worker.loadLanguage(language);
    await worker.initialize(language);
    const {
      data: { text },
    } = await worker.recognize(blob);

    const previewTextDiv: HTMLSpanElement = document.querySelector(
      'div.preview-text-box'
    ) as HTMLDivElement;
    
    previewTextDiv.innerHTML = `<span class='preview-text'>${text}</span>`;
  }
</script>

<!-- svelte-ignore a11y-label-has-associated-control -->
{#await loadLanguages()}
  <span>Loading</span>
{:then languages}
  <main>
    <div class='container'>
      <h1 class='flex-column title'>Eepy Text Extractor</h1>

      <div class='language-selector'>
        <select id='language-selector'>
          {#each languages as language}
            <option value={language.code}>{language.name}</option>
          {/each}
        </select>
      </div>

      <label class='flex-column button-bw button-round'>
        <input
          type='file'
          bind:files={inputFiles}
          on:change={validateInputFile}
        />
        <span>Upload Image</span>
      </label>

      <div class='flex-row preview'>
        <img id='preview-image' src='' alt='' />
        <div class='preview-text-box'>
          <span class='preview-text'>
            How it works: <br>
            Select language that you want to extract text from. <br>
            Upload image and wait for the text to appear. <br>
          </span>
        </div>
      </div>
    </div>
  </main>
{/await}
