export type Language = {
  code: string;
  name: string;
};

export async function parseLanguagesCSV(text: string) {
  const languages: Language[] = [];

  for (const line of text.split("\r\n")) {
    const language_data = line.split(',');

    console.log(language_data);
    
    languages.push({
      code: language_data[0],
      name: language_data[1]
    });
  }

  return languages.slice(3);
}
