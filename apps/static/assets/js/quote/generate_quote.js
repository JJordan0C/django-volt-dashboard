$(function() {
    var selectedChamps = [];
    var selectedMatches = [];
    var matches = undefined;
    var flag_match = false;
    function provideContent(idx, stepDirection, stepPosition, selStep, callback) {
        const CSRF_TOKEN = $("[name='csrfmiddlewaretoken']").val();
        // You can use stepDirection to get ajax content on the forward movement and stepPosition to identify the step position
        if (stepDirection == 'forward' && idx == 1) {
            $('.sw-btn-next').prop('disabled', true);
          // Ajax call to fetch your content
            $.ajax({
            method  : "POST",
            url     : "",
            data: {
                type: "get_matches",
                competition_ids: selectedChamps
            },
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            beforeSend: function( xhr ) {
                // Show the loader
                $('#smartwizard').smartWizard("loader", "show");
            }
            }).done(function( res ) {

                res = res.flat();

                if(!flag_match){
                    /**
                     * Table
                     * Matches
                     */
                    matches = $('#matches').DataTable( {
                        pageLength : 15,
                        dom: 'frtip',
                        responsive: true,
                        autoWidth: false,
                        data: res,
                        columns: [
                            {
                                data: 'id',
                                render: function ( data, type, row, meta ) {
                                    return `<input type="hidden" name="match_id" value="${data}">`
                                }
                            },
                            { data: 'name' },
                            { data: 'competition'}
                        ],
                        columnDefs: [ {
                            orderable: false,
                            className: 'select-checkbox',
                            targets:   0
                        } ],
                        select: {
                            style:    'multi',
                            selector: 'td:first-child'
                        },
                        language: {
                            "infoFiltered": "(filtrati da _MAX_ elementi totali)",
                            "infoThousands": ".",
                            "loadingRecords": "Caricamento...",
                            "processing": "Elaborazione...",
                            "search": "Cerca Partita:",
                            "paginate": {
                                "first": "Inizio",
                                "previous": "Pagina Precedente",
                                "next": "Pagina successiva",
                                "last": "Fine"
                            },
                            "aria": {
                                "sortAscending": ": attiva per ordinare la colonna in ordine crescente",
                                "sortDescending": ": attiva per ordinare la colonna in ordine decrescente"
                            },
                            "autoFill": {
                                "cancel": "Annulla",
                                "fill": "Riempi tutte le celle con <i>%d<\/i>",
                                "fillHorizontal": "Riempi celle orizzontalmente",
                                "fillVertical": "Riempi celle verticalmente"
                            },
                            "buttons": {
                                "collection": "Collezione <span class=\"ui-button-icon-primary ui-icon ui-icon-triangle-1-s\"><\/span>",
                                "colvis": "Visibilità Colonna",
                                "colvisRestore": "Ripristina visibilità",
                                "copy": "Copia",
                                "copyKeys": "Premi ctrl o u2318 + C per copiare i dati della tabella nella tua clipboard di sistema.<br \/><br \/>Per annullare, clicca questo messaggio o premi ESC.",
                                "copySuccess": {
                                    "1": "Copiata 1 riga nella clipboard",
                                    "_": "Copiate %d righe nella clipboard"
                                },
                                "copyTitle": "Copia nella Clipboard",
                                "csv": "CSV",
                                "excel": "Excel",
                                "pageLength": {
                                    "-1": "Mostra tutte le righe",
                                    "_": "Mostra %d righe"
                                },
                                "pdf": "PDF",
                                "print": "Stampa",
                                "createState": "Crea stato",
                                "removeAllStates": "Rimuovi tutti gli stati",
                                "removeState": "Rimuovi",
                                "renameState": "Rinomina",
                                "savedStates": "Salva stato",
                                "stateRestore": "Ripristina stato",
                                "updateState": "Aggiorna"
                            },
                            "emptyTable": "Nessun dato disponibile nella tabella",
                            "info": "Risultati da _START_ a _END_ di _TOTAL_ elementi",
                            "infoEmpty": "Risultati da 0 a 0 di 0 elementi",
                            "lengthMenu": "Mostra _MENU_ elementi",
                            "searchBuilder": {
                                "add": "Aggiungi Condizione",
                                "button": {
                                    "0": "Generatore di Ricerca",
                                    "_": "Generatori di Ricerca (%d)"
                                },
                                "clearAll": "Pulisci Tutto",
                                "condition": "Condizione",
                                "conditions": {
                                    "date": {
                                        "after": "Dopo",
                                        "before": "Prima",
                                        "between": "Tra",
                                        "empty": "Vuoto",
                                        "equals": "Uguale A",
                                        "not": "Non",
                                        "notBetween": "Non Tra",
                                        "notEmpty": "Non Vuoto"
                                    },
                                    "number": {
                                        "between": "Tra",
                                        "empty": "Vuoto",
                                        "equals": "Uguale A",
                                        "gt": "Maggiore Di",
                                        "gte": "Maggiore O Uguale A",
                                        "lt": "Minore Di",
                                        "lte": "Minore O Uguale A",
                                        "not": "Non",
                                        "notBetween": "Non Tra",
                                        "notEmpty": "Non Vuoto"
                                    },
                                    "string": {
                                        "contains": "Contiene",
                                        "empty": "Vuoto",
                                        "endsWith": "Finisce Con",
                                        "equals": "Uguale A",
                                        "not": "Non",
                                        "notEmpty": "Non Vuoto",
                                        "startsWith": "Inizia Con",
                                        "notContains": "Non Contiene",
                                        "notStarts": "Non Inizia Con",
                                        "notEnds": "Non Finisce Con"
                                    },
                                    "array": {
                                        "equals": "Uguale A",
                                        "empty": "Vuoto",
                                        "contains": "Contiene",
                                        "not": "Non",
                                        "notEmpty": "Non Vuoto",
                                        "without": "Senza"
                                    }
                                },
                                "data": "Dati",
                                "deleteTitle": "Elimina regola filtro",
                                "leftTitle": "Criterio di Riduzione Rientro",
                                "logicAnd": "E",
                                "logicOr": "O",
                                "rightTitle": "Criterio di Aumento Rientro",
                                "title": {
                                    "0": "Generatore di Ricerca",
                                    "_": "Generatori di Ricerca (%d)"
                                },
                                "value": "Valore"
                            },
                            "searchPanes": {
                                "clearMessage": "Pulisci Tutto",
                                "collapse": {
                                    "0": "Pannello di Ricerca",
                                    "_": "Pannelli di Ricerca (%d)"
                                },
                                "count": "{total}",
                                "countFiltered": "{shown} ({total})",
                                "emptyPanes": "Nessun Pannello di Ricerca",
                                "loadMessage": "Caricamento Pannello di Ricerca",
                                "title": "Filtri Attivi - %d",
                                "showMessage": "Mostra tutto",
                                "collapseMessage": "Espandi tutto"
                            },
                            "select": {
                                "cells": {
                                    "1": "1 cella selezionata",
                                    "_": "%d celle selezionate"
                                },
                                "columns": {
                                    "1": "1 colonna selezionata",
                                    "_": "%d colonne selezionate"
                                },
                                "rows": {
                                    "1": "1 riga selezionata",
                                    "_": "%d righe selezionate"
                                }
                            },
                            "zeroRecords": "Nessun elemento corrispondente trovato",
                            "datetime": {
                                "amPm": [
                                    "am",
                                    "pm"
                                ],
                                "hours": "ore",
                                "minutes": "minuti",
                                "next": "successivo",
                                "previous": "precedente",
                                "seconds": "secondi",
                                "unknown": "sconosciuto",
                                "weekdays": [
                                    "Dom",
                                    "Lun",
                                    "Mar",
                                    "Mer",
                                    "Gio",
                                    "Ven",
                                    "Sab"
                                ],
                                "months": [
                                    "Gennaio",
                                    "Febbraio",
                                    "Marzo",
                                    "Aprile",
                                    "Maggio",
                                    "Giugno",
                                    "Luglio",
                                    "Agosto",
                                    "Settembre",
                                    "Ottobre",
                                    "Novembre",
                                    "Dicembre"
                                ]
                            },
                            "editor": {
                                "close": "Chiudi",
                                "create": {
                                    "button": "Nuovo",
                                    "submit": "Aggiungi",
                                    "title": "Aggiungi nuovo elemento"
                                },
                                "edit": {
                                    "button": "Modifica",
                                    "submit": "Modifica",
                                    "title": "Modifica elemento"
                                },
                                "error": {
                                    "system": "Errore del sistema."
                                },
                                "multi": {
                                    "info": "Gli elementi selezionati contengono valori diversi. Per modificare e impostare tutti gli elementi per questa selezione allo stesso valore, premi o clicca qui, altrimenti ogni cella manterrà il suo valore attuale.",
                                    "noMulti": "Questa selezione può essere modificata individualmente, ma non se fa parte di un gruppo.",
                                    "restore": "Annulla le modifiche",
                                    "title": "Valori multipli"
                                },
                                "remove": {
                                    "button": "Rimuovi",
                                    "confirm": {
                                        "_": "Sei sicuro di voler cancellare %d righe?",
                                        "1": "Sei sicuro di voler cancellare 1 riga?"
                                    },
                                    "submit": "Rimuovi",
                                    "title": "Rimuovi"
                                }
                            },
                            "thousands": ".",
                            "decimal": ",",
                            "stateRestore": {
                                "creationModal": {
                                    "button": "Crea",
                                    "columns": {
                                        "search": "Colonna Cerca",
                                        "visible": "Colonna Visibilità"
                                    },
                                    "name": "Nome:",
                                    "order": "Ordinamento",
                                    "paging": "Paginazione",
                                    "scroller": "Scorri posizione",
                                    "search": "Ricerca",
                                    "searchBuilder": "Form di Ricerca",
                                    "select": "Seleziona",
                                    "title": "Crea nuovo Stato",
                                    "toggleLabel": "Includi:"
                                },
                                "duplicateError": "Nome stato già presente",
                                "emptyError": "Il nome è obbligatorio",
                                "emptyStates": "Non ci sono stati salvati",
                                "removeConfirm": "Sei sicuro di eliminare lo Stato %s?",
                                "removeError": "Errore durante l'eliminazione dello Stato",
                                "removeJoiner": "e",
                                "removeSubmit": "Elimina",
                                "removeTitle": "Elimina Stato",
                                "renameButton": "Rinomina",
                                "renameLabel": "Nuovo nome per %s:",
                                "renameTitle": "Rinomina Stato"
                            }
                        },
                        order: [[ 1, 'asc' ]]
                    } );

                    flag_match = true;
                }else{
                    matches.clear();
                    matches.rows.add(res);
                    matches.draw();
                }

                if(matches != undefined){
                    matches.on("click", "th#match", function() {
                        if ($("th#match").hasClass("selected")){
                            $("th#match > input").prop('checked', false);
                            matches.rows().deselect();
                            $("th#match").removeClass("selected");
                        }else{
                            $("th#match > input").prop('checked', true);
                            matches.rows().select();
                            $("th#match").addClass("selected");
                        }
                    }).on("select deselect", function(){
                        if(matches.rows({
                            selected: true
                        }).count() !== matches.rows().count()){
                            $("th#match").removeClass("selected");
                        }else{
                            $("th#match").addClass("selected");  
                        }
                        selectedMatches = []
                        var selectedRows = matches.rows( { selected: true } ).data().toArray();
                        for ( row of selectedRows ){
                            selectedMatches.push(row.id);
                        }
                        if(selectedMatches.length > 0){
                            $('.sw-btn-next').prop('disabled', false);
                        }else{
                            $('.sw-btn-next').prop('disabled', true);
                        }
                    });
                }
                // Hide the loader
                $('#smartwizard').smartWizard("loader", "hide");
                callback('')
            }).fail(function(err) {
                // Handle ajax error
        
                // Hide the loader
                $('#smartwizard').smartWizard("loader", "hide");
            });
        }
        if(idx == 2) {
            $('.sw-btn-next').html('Scarica Quote');
        }else{
            $('.sw-btn-next').html('Avanti');
        }
       
        // The callback must called in any case to procced the steps
        // The empty callback will not apply any dynamic contents to the steps
        callback();
    }

    /**
     * Table
     * Championship
     */

    var champ = $('#championship').DataTable( {
        pageLength : 15,
        dom: 'Bfrtip',
        responsive: true,
        columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            targets:   0,
            checkboxes: {
                selectRow: true
            }
        } ],
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        language: {
            "infoFiltered": "(filtrati da _MAX_ elementi totali)",
            "infoThousands": ".",
            "loadingRecords": "Caricamento...",
            "processing": "Elaborazione...",
            "search": "Cerca Campionato:",
            "paginate": {
                "first": "Inizio",
                "previous": "Pagina Precedente",
                "next": "Pagina successiva",
                "last": "Fine"
            },
            "aria": {
                "sortAscending": ": attiva per ordinare la colonna in ordine crescente",
                "sortDescending": ": attiva per ordinare la colonna in ordine decrescente"
            },
            "autoFill": {
                "cancel": "Annulla",
                "fill": "Riempi tutte le celle con <i>%d<\/i>",
                "fillHorizontal": "Riempi celle orizzontalmente",
                "fillVertical": "Riempi celle verticalmente"
            },
            "buttons": {
                "collection": "Collezione <span class=\"ui-button-icon-primary ui-icon ui-icon-triangle-1-s\"><\/span>",
                "colvis": "Visibilità Colonna",
                "colvisRestore": "Ripristina visibilità",
                "copy": "Copia",
                "copyKeys": "Premi ctrl o u2318 + C per copiare i dati della tabella nella tua clipboard di sistema.<br \/><br \/>Per annullare, clicca questo messaggio o premi ESC.",
                "copySuccess": {
                    "1": "Copiata 1 riga nella clipboard",
                    "_": "Copiate %d righe nella clipboard"
                },
                "copyTitle": "Copia nella Clipboard",
                "csv": "CSV",
                "excel": "Excel",
                "pageLength": {
                    "-1": "Mostra tutte le righe",
                    "_": "Mostra %d righe"
                },
                "pdf": "PDF",
                "print": "Stampa",
                "createState": "Crea stato",
                "removeAllStates": "Rimuovi tutti gli stati",
                "removeState": "Rimuovi",
                "renameState": "Rinomina",
                "savedStates": "Salva stato",
                "stateRestore": "Ripristina stato",
                "updateState": "Aggiorna"
            },
            "emptyTable": "Nessun dato disponibile nella tabella",
            "info": "Risultati da _START_ a _END_ di _TOTAL_ elementi",
            "infoEmpty": "Risultati da 0 a 0 di 0 elementi",
            "lengthMenu": "Mostra _MENU_ elementi",
            "searchBuilder": {
                "add": "Aggiungi Condizione",
                "button": {
                    "0": "Generatore di Ricerca",
                    "_": "Generatori di Ricerca (%d)"
                },
                "clearAll": "Pulisci Tutto",
                "condition": "Condizione",
                "conditions": {
                    "date": {
                        "after": "Dopo",
                        "before": "Prima",
                        "between": "Tra",
                        "empty": "Vuoto",
                        "equals": "Uguale A",
                        "not": "Non",
                        "notBetween": "Non Tra",
                        "notEmpty": "Non Vuoto"
                    },
                    "number": {
                        "between": "Tra",
                        "empty": "Vuoto",
                        "equals": "Uguale A",
                        "gt": "Maggiore Di",
                        "gte": "Maggiore O Uguale A",
                        "lt": "Minore Di",
                        "lte": "Minore O Uguale A",
                        "not": "Non",
                        "notBetween": "Non Tra",
                        "notEmpty": "Non Vuoto"
                    },
                    "string": {
                        "contains": "Contiene",
                        "empty": "Vuoto",
                        "endsWith": "Finisce Con",
                        "equals": "Uguale A",
                        "not": "Non",
                        "notEmpty": "Non Vuoto",
                        "startsWith": "Inizia Con",
                        "notContains": "Non Contiene",
                        "notStarts": "Non Inizia Con",
                        "notEnds": "Non Finisce Con"
                    },
                    "array": {
                        "equals": "Uguale A",
                        "empty": "Vuoto",
                        "contains": "Contiene",
                        "not": "Non",
                        "notEmpty": "Non Vuoto",
                        "without": "Senza"
                    }
                },
                "data": "Dati",
                "deleteTitle": "Elimina regola filtro",
                "leftTitle": "Criterio di Riduzione Rientro",
                "logicAnd": "E",
                "logicOr": "O",
                "rightTitle": "Criterio di Aumento Rientro",
                "title": {
                    "0": "Generatore di Ricerca",
                    "_": "Generatori di Ricerca (%d)"
                },
                "value": "Valore"
            },
            "searchPanes": {
                "clearMessage": "Pulisci Tutto",
                "collapse": {
                    "0": "Pannello di Ricerca",
                    "_": "Pannelli di Ricerca (%d)"
                },
                "count": "{total}",
                "countFiltered": "{shown} ({total})",
                "emptyPanes": "Nessun Pannello di Ricerca",
                "loadMessage": "Caricamento Pannello di Ricerca",
                "title": "Filtri Attivi - %d",
                "showMessage": "Mostra tutto",
                "collapseMessage": "Espandi tutto"
            },
            "select": {
                "cells": {
                    "1": "1 cella selezionata",
                    "_": "%d celle selezionate"
                },
                "columns": {
                    "1": "1 colonna selezionata",
                    "_": "%d colonne selezionate"
                },
                "rows": {
                    "1": "1 riga selezionata",
                    "_": "%d righe selezionate"
                }
            },
            "zeroRecords": "Nessun elemento corrispondente trovato",
            "datetime": {
                "amPm": [
                    "am",
                    "pm"
                ],
                "hours": "ore",
                "minutes": "minuti",
                "next": "successivo",
                "previous": "precedente",
                "seconds": "secondi",
                "unknown": "sconosciuto",
                "weekdays": [
                    "Dom",
                    "Lun",
                    "Mar",
                    "Mer",
                    "Gio",
                    "Ven",
                    "Sab"
                ],
                "months": [
                    "Gennaio",
                    "Febbraio",
                    "Marzo",
                    "Aprile",
                    "Maggio",
                    "Giugno",
                    "Luglio",
                    "Agosto",
                    "Settembre",
                    "Ottobre",
                    "Novembre",
                    "Dicembre"
                ]
            },
            "editor": {
                "close": "Chiudi",
                "create": {
                    "button": "Nuovo",
                    "submit": "Aggiungi",
                    "title": "Aggiungi nuovo elemento"
                },
                "edit": {
                    "button": "Modifica",
                    "submit": "Modifica",
                    "title": "Modifica elemento"
                },
                "error": {
                    "system": "Errore del sistema."
                },
                "multi": {
                    "info": "Gli elementi selezionati contengono valori diversi. Per modificare e impostare tutti gli elementi per questa selezione allo stesso valore, premi o clicca qui, altrimenti ogni cella manterrà il suo valore attuale.",
                    "noMulti": "Questa selezione può essere modificata individualmente, ma non se fa parte di un gruppo.",
                    "restore": "Annulla le modifiche",
                    "title": "Valori multipli"
                },
                "remove": {
                    "button": "Rimuovi",
                    "confirm": {
                        "_": "Sei sicuro di voler cancellare %d righe?",
                        "1": "Sei sicuro di voler cancellare 1 riga?"
                    },
                    "submit": "Rimuovi",
                    "title": "Rimuovi"
                }
            },
            "thousands": ".",
            "decimal": ",",
            "stateRestore": {
                "creationModal": {
                    "button": "Crea",
                    "columns": {
                        "search": "Colonna Cerca",
                        "visible": "Colonna Visibilità"
                    },
                    "name": "Nome:",
                    "order": "Ordinamento",
                    "paging": "Paginazione",
                    "scroller": "Scorri posizione",
                    "search": "Ricerca",
                    "searchBuilder": "Form di Ricerca",
                    "select": "Seleziona",
                    "title": "Crea nuovo Stato",
                    "toggleLabel": "Includi:"
                },
                "duplicateError": "Nome stato già presente",
                "emptyError": "Il nome è obbligatorio",
                "emptyStates": "Non ci sono stati salvati",
                "removeConfirm": "Sei sicuro di eliminare lo Stato %s?",
                "removeError": "Errore durante l'eliminazione dello Stato",
                "removeJoiner": "e",
                "removeSubmit": "Elimina",
                "removeTitle": "Elimina Stato",
                "renameButton": "Rinomina",
                "renameLabel": "Nuovo nome per %s:",
                "renameTitle": "Rinomina Stato"
            }
        },
        order: [[ 1, 'asc' ]]
    } );
    champ.on("click", "th#champ", function() {
        if ($("th#champ").hasClass("selected")){
            $("th#champ > input").prop('checked', false);
            champ.rows().deselect();
            $("th#champ").removeClass("selected");
        }else{
            $("th#champ > input").prop('checked', true);
            champ.rows().select();
            $("th#champ").addClass("selected");
        }
    }).on("select deselect", function(){
        if(champ.rows({
            selected: true
        }).count() !== champ.rows().count()){
            $("th#champ").removeClass("selected");
        }else{
            $("th#champ").addClass("selected");  
        }
        selectedChamps = []
        var selectedRows = champ.rows( { selected: true } ).data().pluck(0).toArray();
        for ( row of selectedRows ){
            selectedChamps.push($(row).val());
        }

        if(selectedChamps.length > 0){
            $('.sw-btn-next').prop('disabled', false);
        }else{
            $('.sw-btn-next').prop('disabled', true);
        }
    });

    /**
     * Table
     * Quote
     */

    $('#quote').DataTable( {
        pageLength : 15,
        dom: 'frtip',
        responsive: true,
        columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            targets:   0
        } ],
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        language: {
            "infoFiltered": "(filtrati da _MAX_ elementi totali)",
            "infoThousands": ".",
            "loadingRecords": "Caricamento...",
            "processing": "Elaborazione...",
            "search": "Cerca Giocata:",
            "paginate": {
                "first": "Inizio",
                "previous": "Pagina Precedente",
                "next": "Pagina successiva",
                "last": "Fine"
            },
            "aria": {
                "sortAscending": ": attiva per ordinare la colonna in ordine crescente",
                "sortDescending": ": attiva per ordinare la colonna in ordine decrescente"
            },
            "autoFill": {
                "cancel": "Annulla",
                "fill": "Riempi tutte le celle con <i>%d<\/i>",
                "fillHorizontal": "Riempi celle orizzontalmente",
                "fillVertical": "Riempi celle verticalmente"
            },
            "buttons": {
                "collection": "Collezione <span class=\"ui-button-icon-primary ui-icon ui-icon-triangle-1-s\"><\/span>",
                "colvis": "Visibilità Colonna",
                "colvisRestore": "Ripristina visibilità",
                "copy": "Copia",
                "copyKeys": "Premi ctrl o u2318 + C per copiare i dati della tabella nella tua clipboard di sistema.<br \/><br \/>Per annullare, clicca questo messaggio o premi ESC.",
                "copySuccess": {
                    "1": "Copiata 1 riga nella clipboard",
                    "_": "Copiate %d righe nella clipboard"
                },
                "copyTitle": "Copia nella Clipboard",
                "csv": "CSV",
                "excel": "Excel",
                "pageLength": {
                    "-1": "Mostra tutte le righe",
                    "_": "Mostra %d righe"
                },
                "pdf": "PDF",
                "print": "Stampa",
                "createState": "Crea stato",
                "removeAllStates": "Rimuovi tutti gli stati",
                "removeState": "Rimuovi",
                "renameState": "Rinomina",
                "savedStates": "Salva stato",
                "stateRestore": "Ripristina stato",
                "updateState": "Aggiorna"
            },
            "emptyTable": "Nessun dato disponibile nella tabella",
            "info": "Risultati da _START_ a _END_ di _TOTAL_ elementi",
            "infoEmpty": "Risultati da 0 a 0 di 0 elementi",
            "lengthMenu": "Mostra _MENU_ elementi",
            "searchBuilder": {
                "add": "Aggiungi Condizione",
                "button": {
                    "0": "Generatore di Ricerca",
                    "_": "Generatori di Ricerca (%d)"
                },
                "clearAll": "Pulisci Tutto",
                "condition": "Condizione",
                "conditions": {
                    "date": {
                        "after": "Dopo",
                        "before": "Prima",
                        "between": "Tra",
                        "empty": "Vuoto",
                        "equals": "Uguale A",
                        "not": "Non",
                        "notBetween": "Non Tra",
                        "notEmpty": "Non Vuoto"
                    },
                    "number": {
                        "between": "Tra",
                        "empty": "Vuoto",
                        "equals": "Uguale A",
                        "gt": "Maggiore Di",
                        "gte": "Maggiore O Uguale A",
                        "lt": "Minore Di",
                        "lte": "Minore O Uguale A",
                        "not": "Non",
                        "notBetween": "Non Tra",
                        "notEmpty": "Non Vuoto"
                    },
                    "string": {
                        "contains": "Contiene",
                        "empty": "Vuoto",
                        "endsWith": "Finisce Con",
                        "equals": "Uguale A",
                        "not": "Non",
                        "notEmpty": "Non Vuoto",
                        "startsWith": "Inizia Con",
                        "notContains": "Non Contiene",
                        "notStarts": "Non Inizia Con",
                        "notEnds": "Non Finisce Con"
                    },
                    "array": {
                        "equals": "Uguale A",
                        "empty": "Vuoto",
                        "contains": "Contiene",
                        "not": "Non",
                        "notEmpty": "Non Vuoto",
                        "without": "Senza"
                    }
                },
                "data": "Dati",
                "deleteTitle": "Elimina regola filtro",
                "leftTitle": "Criterio di Riduzione Rientro",
                "logicAnd": "E",
                "logicOr": "O",
                "rightTitle": "Criterio di Aumento Rientro",
                "title": {
                    "0": "Generatore di Ricerca",
                    "_": "Generatori di Ricerca (%d)"
                },
                "value": "Valore"
            },
            "searchPanes": {
                "clearMessage": "Pulisci Tutto",
                "collapse": {
                    "0": "Pannello di Ricerca",
                    "_": "Pannelli di Ricerca (%d)"
                },
                "count": "{total}",
                "countFiltered": "{shown} ({total})",
                "emptyPanes": "Nessun Pannello di Ricerca",
                "loadMessage": "Caricamento Pannello di Ricerca",
                "title": "Filtri Attivi - %d",
                "showMessage": "Mostra tutto",
                "collapseMessage": "Espandi tutto"
            },
            "select": {
                "cells": {
                    "1": "1 cella selezionata",
                    "_": "%d celle selezionate"
                },
                "columns": {
                    "1": "1 colonna selezionata",
                    "_": "%d colonne selezionate"
                },
                "rows": {
                    "1": "1 riga selezionata",
                    "_": "%d righe selezionate"
                }
            },
            "zeroRecords": "Nessun elemento corrispondente trovato",
            "datetime": {
                "amPm": [
                    "am",
                    "pm"
                ],
                "hours": "ore",
                "minutes": "minuti",
                "next": "successivo",
                "previous": "precedente",
                "seconds": "secondi",
                "unknown": "sconosciuto",
                "weekdays": [
                    "Dom",
                    "Lun",
                    "Mar",
                    "Mer",
                    "Gio",
                    "Ven",
                    "Sab"
                ],
                "months": [
                    "Gennaio",
                    "Febbraio",
                    "Marzo",
                    "Aprile",
                    "Maggio",
                    "Giugno",
                    "Luglio",
                    "Agosto",
                    "Settembre",
                    "Ottobre",
                    "Novembre",
                    "Dicembre"
                ]
            },
            "editor": {
                "close": "Chiudi",
                "create": {
                    "button": "Nuovo",
                    "submit": "Aggiungi",
                    "title": "Aggiungi nuovo elemento"
                },
                "edit": {
                    "button": "Modifica",
                    "submit": "Modifica",
                    "title": "Modifica elemento"
                },
                "error": {
                    "system": "Errore del sistema."
                },
                "multi": {
                    "info": "Gli elementi selezionati contengono valori diversi. Per modificare e impostare tutti gli elementi per questa selezione allo stesso valore, premi o clicca qui, altrimenti ogni cella manterrà il suo valore attuale.",
                    "noMulti": "Questa selezione può essere modificata individualmente, ma non se fa parte di un gruppo.",
                    "restore": "Annulla le modifiche",
                    "title": "Valori multipli"
                },
                "remove": {
                    "button": "Rimuovi",
                    "confirm": {
                        "_": "Sei sicuro di voler cancellare %d righe?",
                        "1": "Sei sicuro di voler cancellare 1 riga?"
                    },
                    "submit": "Rimuovi",
                    "title": "Rimuovi"
                }
            },
            "thousands": ".",
            "decimal": ",",
            "stateRestore": {
                "creationModal": {
                    "button": "Crea",
                    "columns": {
                        "search": "Colonna Cerca",
                        "visible": "Colonna Visibilità"
                    },
                    "name": "Nome:",
                    "order": "Ordinamento",
                    "paging": "Paginazione",
                    "scroller": "Scorri posizione",
                    "search": "Ricerca",
                    "searchBuilder": "Form di Ricerca",
                    "select": "Seleziona",
                    "title": "Crea nuovo Stato",
                    "toggleLabel": "Includi:"
                },
                "duplicateError": "Nome stato già presente",
                "emptyError": "Il nome è obbligatorio",
                "emptyStates": "Non ci sono stati salvati",
                "removeConfirm": "Sei sicuro di eliminare lo Stato %s?",
                "removeError": "Errore durante l'eliminazione dello Stato",
                "removeJoiner": "e",
                "removeSubmit": "Elimina",
                "removeTitle": "Elimina Stato",
                "renameButton": "Rinomina",
                "renameLabel": "Nuovo nome per %s:",
                "renameTitle": "Rinomina Stato"
            }
        },
        order: [[ 1, 'asc' ]]
    } );

    $('.select-item:not(:first-child)').hide()

    $('#smartwizard').smartWizard(
        {
            lang: {
                next: 'Avanti',
                previous: 'Indietro'
            },
            toolbar: {
                position: 'both',
              },
            getContent: provideContent,
            enableUrlHash: false
        }
    );
    $('.sw-btn-next').prop('disabled', true)
});