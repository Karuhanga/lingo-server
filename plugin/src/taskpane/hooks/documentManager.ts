import {fixAnsiUtf8Issue} from "../../utils";

interface DocumentManager {
    getWords();
}

export function useDocumentManager(setDebug?): DocumentManager {
    function getDocumentWords() {
        return Word.run(async context => {
            const doc = context.document.body.getHtml();
            await context.sync();
            const docContent = fixAnsiUtf8Issue(doc.value);

            const htmlContent = new DOMParser().parseFromString(docContent, "text/html").body.innerText;
            if (setDebug) setDebug(docContent);
            return unique(removeSpaces(htmlContent.toLowerCase().split(/\s+/)));
        });
    }

    return {
        getWords: getDocumentWords,
    }
}

function unique(arr: string[]) {
    const u = {};
    return arr.filter((v) => {
        return u[v] = !u.hasOwnProperty(v);
    });
}

function removeSpaces(words: string[]) {
    return words.map(word => word.trim()).filter(word => !!word);
}
