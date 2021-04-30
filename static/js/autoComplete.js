(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
    typeof define === 'function' && define.amd ? define(factory) :
    (global.autoComplete = factory());
  }(this, (function () { 'use strict';

    function _classCallCheck(instance, Constructor) {
      if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
      }
    }

    function _defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    function _createClass(Constructor, protoProps, staticProps) {
      if (protoProps) _defineProperties(Constructor.prototype, protoProps);
      if (staticProps) _defineProperties(Constructor, staticProps);
      return Constructor;
    }

    var dataAttribute = "data-result";
    var select = {
      resultsList: "autoComplete_results_list",
      result: "autoComplete_result",
      highlight: "autoComplete_highlighted"
    };
    var getInput = function getInput(selector) {
      return typeof selector === "string" ? document.querySelector(selector) : selector();
    };
    var createResultsList = function createResultsList(renderResults) {
      var resultsList = document.createElement("ul");
      if (renderResults.container) {
        select.resultsList = renderResults.container(resultsList) || select.resultsList;
      }
      resultsList.setAttribute("id", select.resultsList);
      renderResults.destination.insertAdjacentElement(renderResults.position, resultsList);
      return resultsList;
    };
    var highlight = function highlight(value) {
      return "<span class=".concat(select.highlight, ">").concat(value, "</span>");
    };
    var addResultsToList = function addResultsToList(resultsList, dataSrc, dataKey, callback) {
      dataSrc.forEach(function (event, record) {
        var result = document.createElement("li");
        var resultValue = dataSrc[record].value[event.key] || dataSrc[record].value;
        result.setAttribute(dataAttribute, resultValue);
        result.setAttribute("class", select.result);
        result.setAttribute("tabindex", "1");
        result.innerHTML = callback ? callback(event, result) : event.match || event;
        resultsList.appendChild(result);
      });
    };
    var navigation = function navigation(selector, resultsList) {
      var input = getInput(selector);
      var first = resultsList.firstChild;
      document.onkeydown = function (event) {
        var active = document.activeElement;
        switch (event.keyCode) {
          case 38:
            if (active !== first && active !== input) {
              active.previousSibling.focus();
            } else if (active === first) {
              input.focus();
            }
            break;
          case 40:
            if (active === input && resultsList.childNodes.length > 0) {
              first.focus();
            } else if (active !== resultsList.lastChild) {
              active.nextSibling.focus();
            }
            break;
        }
      };
    };
    var clearResults = function clearResults(resultsList) {
      return resultsList.innerHTML = "";
    };
    var getSelection = function getSelection(field, resultsList, callback, resultsValues) {
      var results = resultsList.querySelectorAll(".".concat(select.result));
      Object.keys(results).forEach(function (selection) {
        ["mousedown", "keydown"].forEach(function (eventType) {
          results[selection].addEventListener(eventType, function (event) {
            if (eventType === "mousedown" || event.keyCode === 13 || event.keyCode === 39) {
              callback({
                event: event,
                query: getInput(field).value,
                matches: resultsValues.matches,
                results: resultsValues.list.map(function (record) {
                  return record.value;
                }),
                selection: resultsValues.list.find(function (value) {
                  var resValue = value.value[value.key] || value.value;
                  return resValue === event.target.closest(".".concat(select.result)).getAttribute(dataAttribute);
                })
              });
              clearResults(resultsList);
            }
          });
        });
      });
    };
    var autoCompleteView = {
      getInput: getInput,
      createResultsList: createResultsList,
      highlight: highlight,
      addResultsToList: addResultsToList,
      navigation: navigation,
      clearResults: clearResults,
      getSelection: getSelection
    };

    var autoComplete =
    function () {
      function autoComplete(config) {
        _classCallCheck(this, autoComplete);
        this.selector = config.selector || "#autoComplete";
        this.data = {
          src: function src() {
            return typeof config.data.src === "function" ? config.data.src() : config.data.src;
          },
          key: config.data.key
        };
        this.searchEngine = config.searchEngine === "loose" ? "loose" : "strict";
        this.threshold = config.threshold || 0;
        this.resultsList = autoCompleteView.createResultsList({
          container: config.resultsList && config.resultsList.container ? config.resultsList.container : false,
          destination: config.resultsList && config.resultsList.destination ? config.resultsList.destination : autoCompleteView.getInput(this.selector),
          position: config.resultsList && config.resultsList.position ? config.resultsList.position : "afterend"
        });
        this.sort = config.sort || false;
        this.placeHolder = config.placeHolder;
        this.maxResults = config.maxResults || 5;
        this.resultItem = config.resultItem;
        this.highlight = config.highlight || false;
        this.onSelection = config.onSelection;
        this.init();
      }
      _createClass(autoComplete, [{
        key: "search",
        value: function search(query, record) {
          var highlight = this.highlight;
          var recordLowerCase = record.toString().toLowerCase();
          if (this.searchEngine === "loose") {
            query = query.replace(/ /g, "");
            var match = [];
            var searchPosition = 0;
            for (var number = 0; number < recordLowerCase.length; number++) {
              var recordChar = record[number];
              if (searchPosition < query.length && recordLowerCase[number] === query[searchPosition]) {
                recordChar = highlight ? autoCompleteView.highlight(recordChar) : recordChar;
                searchPosition++;
              }
              match.push(recordChar);
            }
            if (searchPosition !== query.length) {
              return false;
            }
            return match.join("");
          } else {
            if (recordLowerCase.includes(query)) {
              var pattern = new RegExp("".concat(query), "i");
              query = pattern.exec(record);
              return highlight ? record.replace(query, autoCompleteView.highlight(query)) : record;
            }
          }
        }
      }, {
        key: "listMatchedResults",
        value: function listMatchedResults(data) {
          var _this = this;
          var resList = [];
          var inputValue = autoCompleteView.getInput(this.selector).value.toLowerCase();
          data.filter(function (record, index) {
            var search = function search(key) {
              var match = _this.search(inputValue, record[key] || record);
              if (match && key) {
                resList.push({
                  key: key,
                  index: index,
                  match: match,
                  value: record
                });
              } else if (match && !key) {
                resList.push({
                  index: index,
                  match: match,
                  value: record
                });
              }
            };
            if (_this.data.key) {
              var _iteratorNormalCompletion = true;
              var _didIteratorError = false;
              var _iteratorError = undefined;
              try {
                for (var _iterator = _this.data.key[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                  var key = _step.value;
                  search(key);
                }
              } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
              } finally {
                try {
                  if (!_iteratorNormalCompletion && _iterator.return != null) {
                    _iterator.return();
                  }
                } finally {
                  if (_didIteratorError) {
                    throw _iteratorError;
                  }
                }
              }
            } else {
              search();
            }
          });
          var list = this.sort ? resList.sort(this.sort).slice(0, this.maxResults) : resList.slice(0, this.maxResults);
          autoCompleteView.addResultsToList(this.resultsList, list, this.data.key, this.resultItem);
          autoCompleteView.navigation(this.selector, this.resultsList);
          return {
            matches: resList.length,
            list: list
          };
        }
      }, {
        key: "ignite",
        value: function ignite(data) {
          var _this2 = this;
          var selector = this.selector;
          var input = autoCompleteView.getInput(selector);
          var placeHolder = this.placeHolder;
          var onSelection = this.onSelection;
          if (placeHolder) {
            input.setAttribute("placeholder", placeHolder);
          }
          input.onkeyup = function (event) {
            var resultsList = _this2.resultsList;
            var clearResults = autoCompleteView.clearResults(resultsList);
            if (input.value.length > _this2.threshold && input.value.replace(/ /g, "").length) {
              var list = _this2.listMatchedResults(data);
              input.dispatchEvent(new CustomEvent("type", {
                bubbles: true,
                detail: {
                  event: event,
                  query: input.value,
                  matches: list.matches,
                  results: list.list
                },
                cancelable: true
              }));
              if (onSelection) {
                autoCompleteView.getSelection(selector, resultsList, onSelection, list);
              }
            }
          };
        }
      }, {
        key: "init",
        value: function init() {
          var _this3 = this;
          var dataSrc = this.data.src();
          if (dataSrc instanceof Promise) {
            dataSrc.then(function (data) {
              return _this3.ignite(data);
            });
          } else {
            this.ignite(dataSrc);
          }
        }
      }]);
      return autoComplete;
    }();

    return autoComplete;

  })));
