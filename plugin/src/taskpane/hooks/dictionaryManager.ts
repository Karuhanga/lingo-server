import {useState} from "react";

interface DictionaryManagerStatusInfo {
    weHaveADictionary: boolean;
}

export function dictionaryManager(): DictionaryManagerStatusInfo {
    const [weHaveADictionary] = useState(true);

    return {weHaveADictionary};
}
