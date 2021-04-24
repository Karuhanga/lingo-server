import {Button, ButtonType, DefaultButton} from "office-ui-fabric-react";
import * as React from "react";
import InsertLocation = Word.InsertLocation;

export interface WrongWord {wrong: string, suggestions: string[]}

export interface SingleWrongWordProps {
    wrongWord: WrongWord;
    index: number;
    removeWord(wrongWord: string): void;
    setDebug?(message: string): void;
}

export function SingleWrongWord({wrongWord, index, removeWord, setDebug}: SingleWrongWordProps) {
    const firstSuggestion = wrongWord.suggestions[0];
    const weHaveSuggestions = !!firstSuggestion;
    return (
        <tr key={index}>
            <td>
                <DefaultButton
                    split
                    style={{width: "100%", border: "0"}}
                    menuIconProps={{iconName: "__nonExistent__"}}
                    text={wrongWord.wrong}
                    menuProps={{
                        items: [
                            {
                                key: 'addToPrivateDictionary',
                                text: 'Add to my dictionary',
                                iconProps: { iconName: 'Add' },
                            },
                            {
                                key: 'addToGlobalDictionary',
                                text: 'Propose Word',
                                iconProps: { iconName: 'World' },
                            },
                        ],
                    }}
                    // onClick={_alertClicked}
                />
            </td>
            <td>&nbsp;&nbsp;{weHaveSuggestions ? " → " : ""}&nbsp;&nbsp;</td>
            <td>
                {!weHaveSuggestions ?  "" : (
                    <DefaultButton
                        split
                        style={{width: "100%", border: "0"}}
                        menuIconProps={{iconName: "__nonExistent__"}}
                        text={firstSuggestion}
                        menuProps={{
                            items: wrongWord.suggestions.map(suggestion => ({
                                key: suggestion,
                                text: suggestion,
                                onClick: () => replaceWord(wrongWord.wrong, suggestion, removeWord, setDebug),
                            })),
                        }}
                    />
                )}
            </td>
            <td>
                {!weHaveSuggestions ? null : (
                    <Button
                        buttonType={ButtonType.icon}
                        iconProps={{ iconName: "CheckMark" }}
                        onClick={() => replaceWord(wrongWord.wrong, firstSuggestion, removeWord, setDebug)}
                    />
                )}
            </td>
        </tr>
    )
}

function replaceWord(word: string, replacement: string, removeWord: (wrongWord: string) => void, setDebug?) {
    Word.run(async function (context) {
        const searchResults = context.document.body.search(word, {ignorePunct: true, matchWholeWord: true});
        context.load(searchResults);
        await context.sync();

        if (setDebug) setDebug(JSON.stringify(searchResults.toJSON()));

        searchResults.items.forEach(item => {
            item.insertText(replacement, InsertLocation.replace);
        });

        // Synchronize the document state by executing the queued commands,
        // and return a promise to indicate task completion.
        await context.sync();
        removeWord(word);
    })
}
