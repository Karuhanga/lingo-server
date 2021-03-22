import * as React from "react";
import {Button, ButtonType, DefaultButton} from "office-ui-fabric-react";
import InsertLocation = Word.InsertLocation;

export interface WrongWord {wrong: string, suggestions: string[]}

export interface WrongWordListProps {
  message: string;
  items: WrongWord[];
  recheck(): void;
  recheckDisabled: boolean;
  removeWord(wrongWord: string): void;
  setDebug?(message: string): void;
}

export default class WrongWordList extends React.Component<WrongWordListProps> {
  render() {
    const { items, message, recheck, recheckDisabled, removeWord, setDebug } = this.props;

    return (
      <main className="ms-welcome__main">
        <h2 className="ms-font-xl ms-fontWeight-semilight ms-fontColor-neutralPrimary ms-u-slideUpIn20">
            {message}
            &nbsp;
            <Button
                buttonType={ButtonType.icon}
                iconProps={{ iconName: "Refresh" }}
                onClick={recheck}
                disabled={recheckDisabled}
            >
                Recheck
            </Button>
        </h2>
        <table className="ms-font-m ms-fontColor-neutralPrimary">
          {
              items.map((item, index) => {
                  const firstSuggestion = item.suggestions[0];
                  const weHaveSuggestions = !!firstSuggestion;
                  return (
                      <tr key={index}>
                          <td>
                              <DefaultButton
                                  split
                                  style={{width: "100%", border: "0"}}
                                  menuIconProps={{iconName: "__nonExistent__"}}
                                  text={item.wrong}
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
                                          items: item.suggestions.map(suggestion => ({
                                              key: suggestion,
                                              text: suggestion,
                                              onClick: () => replaceWord(item.wrong, suggestion, removeWord, setDebug),
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
                                      onClick={() => replaceWord(item.wrong, firstSuggestion, removeWord, setDebug)}
                                  />
                              )}
                          </td>
                      </tr>
                  )
              })
          }
        </table>
      </main>
    );
  }
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
