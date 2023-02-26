package com.shytaani.vfts.service;

import java.util.Arrays;
import java.util.List;

import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.stereotype.Service;

import com.shytaani.vfts.dao.CardMapper;
import com.shytaani.vfts.dto.Card;
import com.shytaani.vfts.entity.Word;
import com.shytaani.vfts.exception.NoSuchCardException;

@Service
public class VftsService {

    private final CardMapper mapper;

    private final MessageSource messageSource;
    
    public VftsService(CardMapper mapper, MessageSource messageSource) {
        this.mapper = mapper;
        this.messageSource = messageSource;
    }

    public List<Card> getCards() {
        List<Word> words = mapper.findWords();
        return words.stream().map(word -> {
            List<String> definitions = mapper.findDefinitions(word.id())
                .stream()
                .map(definition -> definition.definition())
                .toList();
            List<String> sentences = mapper.findSentences(word.id())
                .stream()
                .map(sentence -> sentence.sentence())
                .toList();
            return new Card(word.id(), word.word(), definitions, sentences);
        }).toList();
    }

    public Card getCard(int id) throws NoSuchCardException {
        Word word = mapper.findWord(id).orElseThrow(() -> 
            new NoSuchCardException(messageSource.getMessage("no.such.card", new Integer[]{id}, LocaleContextHolder.getLocale())));
        List<String> definitions = mapper.findDefinitions(word.id())
            .stream()
            .map(definition -> definition.definition())
            .toList();
        List<String> sentences = mapper.findSentences(word.id())
            .stream()
            .map(sentence -> sentence.sentence())
            .toList();
        return new Card(word.id(), word.word(), definitions, sentences);
    }
}
