from app.main import parse_quoted_str, tokenize_quote


class TestParseQuotedStr:
    def test_single_quotes(self):
        assert parse_quoted_str("'shell hello'") == "shell hello"
        assert parse_quoted_str("'world     test'") == "world     test"
        assert parse_quoted_str("'hello    world'") == "hello    world"
        assert parse_quoted_str("hello    world") == "hello world"
        assert parse_quoted_str("'hello''world'") == "helloworld"
        assert parse_quoted_str("hello''world") == "helloworld"
        
    def test_double_quotes(self):
        assert parse_quoted_str('"quz  hello"  "bar"') == "quz  hello bar"
        assert parse_quoted_str('"bar"  "shell\'s"  "foo"') == "bar shell\'s foo"
        
    def test_backslash_outside_quotes(self):
        # assert parse_quoted_str(r'"before\   after"') == r"before\   after"
        assert parse_quoted_str(r'world\ \ \ \ \ \ script') == "world      script"
        
    def test_backslash_within_single_quotes(self):
        assert parse_quoted_str(r"'shell\\\nscript'") == r"shell\\\nscript"
        assert parse_quoted_str(r"'example\"testhello\"shell'") == r"example\"testhello\"shell"

    def test_backslash_within_double_quotes(self):
        assert parse_quoted_str(r""" "hello'script'\\n'world" """) == r" hello'script'\n'world "
        assert parse_quoted_str(r""" "hello\"insidequotes"script\" """) == ' hello"insidequotesscript" '


class TestTokenizeQuote:
    def test_tokenize_single_quoted_str(self):
        # https://app.codecrafters.io/courses/shell/stages/ni6?repo=9694458a-49ce-45d2-a57d-5964670b8257&track=python
        assert tokenize_quote(r"""'/tmp/file name' '/tmp/file name with spaces'""") == [
            "/tmp/file name",
            "/tmp/file name with spaces",
        ]
        
    def test_tokenize_double_quoted_str(self):
        # https://app.codecrafters.io/courses/shell/stages/tg6?repo=9694458a-49ce-45d2-a57d-5964670b8257&track=python
        assert tokenize_quote(r'''"/tmp/file name" "/tmp/'file name' with spaces"''') == [
            "/tmp/file name",
            "/tmp/'file name' with spaces",
        ]
        
    def test_tokenize_quote_with_backslash_outside_quotes(self):
        # https://app.codecrafters.io/courses/shell/stages/tg6?repo=9694458a-49ce-45d2-a57d-5964670b8257&track=python
        assert tokenize_quote(r'''"/tmp/file\\name" "/tmp/file\ name"''') == [
            r"/tmp/file\name",
            r"/tmp/file\ name"
        ]
        
    def test_tokenize_quote_with_backslash_within_single_quoted_str(self):
        # https://app.codecrafters.io/courses/shell/stages/le5?repo=9694458a-49ce-45d2-a57d-5964670b8257&track=python
        assert tokenize_quote(r'''"/tmp/file/'name'" "/tmp/file/'\name\'"''') == [
            r"/tmp/file/'name'",
            r"/tmp/file/'\name\'"
        ]
        
    def test_tokenize_quote_with_backslash_within_double_quote(self):
        # https://app.codecrafters.io/courses/shell/stages/gu3?repo=9694458a-49ce-45d2-a57d-5964670b8257&track=python
        assert tokenize_quote(r'''"/tmp/ant/\"f 38\"" "/tmp/ant/\"f\\93\""''') == [
            r'/tmp/ant/"f 38"',
            r'/tmp/ant/"f\93"',
        ]
        
    def test_tokenize_double_quoted_str_with_backslash(self):
        assert tokenize_quote(r""" "/tmp/dog/'f 87'" "/tmp/dog/'f  \98'" "/tmp/dog/'f \42\'" """) == [
            "/tmp/dog/'f 87'",
            r"/tmp/dog/'f  \98'",
            r"/tmp/dog/'f \42\'"
        ]