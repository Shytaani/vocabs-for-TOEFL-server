package com.shytaani.vfts.controller;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;

import com.shytaani.vfts.dto.Card;
import com.shytaani.vfts.exception.NoSuchCardException;
import com.shytaani.vfts.service.VftsService;

@SpringBootTest
public class VftsControllerTests {
    
    @Mock
    private VftsService service;

    @InjectMocks
    private VftsController controller;

    @Test
    void getCardsReturnsCardList() {
        when(service.getCards()).thenReturn(List.of(
            new Card(1, "word1", List.of("def1", "def2"), List.of("sen1", "sen2")),
            new Card(2, "word2", List.of("def3"), List.of("sen3"))
        ));

        List<Card> cards = controller.getCards();

        assertAll(() -> {
            assertEquals(2, cards.size());
            assertEquals("word1", cards.get(0).word());
            assertEquals(2, cards.get(0).definitions().size());
            assertEquals("def1", cards.get(0).definitions().get(0));
            assertEquals("def2", cards.get(0).definitions().get(1));
            assertEquals(2, cards.get(0).sentences().size());
            assertEquals("sen1", cards.get(0).sentences().get(0));
            assertEquals("sen2", cards.get(0).sentences().get(1));

            assertEquals("word2", cards.get(1).word());
            assertEquals(1, cards.get(1).definitions().size());
            assertEquals("def3", cards.get(1).definitions().get(0));
            assertEquals(1, cards.get(1).sentences().size());
            assertEquals("sen3", cards.get(1).sentences().get(0));
        });
    }

    @Test
    void getCardsReturnsEmptyList() {
        when(service.getCards()).thenReturn(List.of());

        List<Card> cards = controller.getCards();

        assertEquals(0, cards.size());
    }

    @Test
    void getCardReturnsACard() throws NoSuchCardException {
        when(service.getCard(1)).thenReturn(
            new Card(1, "word1", List.of("def1", "def2"), List.of("sen1", "sen2"))
        );

        Card card = controller.getCard(1);

        assertAll(() -> {
            assertEquals("word1", card.word());
            assertEquals(2, card.definitions().size());
            assertEquals("def1", card.definitions().get(0));
            assertEquals("def2", card.definitions().get(1));
            assertEquals(2, card.sentences().size());
            assertEquals("sen1", card.sentences().get(0));
            assertEquals("sen2", card.sentences().get(1));
        });
    }

    @Test
    void getCardThorwsNoSuchCardException() throws NoSuchCardException {
        when(service.getCard(1)).thenThrow(NoSuchCardException.class);

        assertThrows(NoSuchCardException.class, () -> controller.getCard(1));
    }
}
