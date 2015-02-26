# UFUInfo

UFUInfo é uma "biblioteca" Python (2.7) capaz de recuperar informações disponíveis nos sites da UFU, a Universidade Federal de Uberlândia. Seus *parsers* retornam *dictionaries* (ou *lists* desses) devidamente aninhados, seguindo os padrões definidos pela documentação. Nenhuma "lógica de negócio" é feita por ela, sendo apenas uma interface para os serviços existentes.

Há um script de exemplos na raiz do repositório, já que este projeto não vale documentação detalhada.

Sinta-se à vontade para contribuir, seja reportando erros, otimizando código, implementando ou sugerindo recursos.

## Licença

UFUInfo é licenciada sob a LGPL v3.

## Recursos

Os itens marcados já estão em um estágio considerado útil

- **Parsers** - Processar e organizar dados
  - Restaurante Universitário
    - [x] Cardápio
    - [ ] Comunicados
    - [x] Informações
  - Biblioteca
    - [ ] Consulta ao catálogo
    - [ ] Comunicados
    - [ ] Informações

- **Actions**
  - Biblioteca
    - [ ] Renovação de empréstimo

## Dependências

UFUInfo depende da biblioteca Beautiful Soup 4, da unidecode e, obviamente, de uma conexão com a Internet.
