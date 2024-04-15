from django.test import TestCase
from django.urls import reverse

class TestHomePageMessage(TestCase):

    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home') # using name from urls
        response = self.client.get(url)
        self.assertContains(response, 'Music Videos') # checking to see iff the string is present


class TestAddVideos(TestCase):

    def test_add_video(self):

        valid_video = {
            'name' : 'The Buggles - Video Killed The Radio Star (Official Music Video)',
            'url' : 'https://www.youtube.com/watch?v=W8r-tXRLazs',
            'notes': 'ironic aint it?'
        }

        url = reverse('add_video')
        # follow=True -> if site is redirected to new page during the request allow that to happen without failing the test
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        # does the video list actually show the new video?
        self.assertContains(response, 'The Buggles - Video Killed The Radio Star (Official Music Video)')
        self.assertContains(response, 'ironic aint it?')
        self.assertContains(response, 'https://www.youtube.com/watch?v=W8r-tXRLazs')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count) # does the DB now have one video?

        # is the video that got stored in the DB the actual video submitted?
        # should only be one video in the DB so free to use the below:
        video = Video.objects.first()

        self.assertEqual('The Buggles - Video Killed The Radio Star (Official Music Video)', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=W8r-tXRLazs', video.url)
        self.assertEqual('ironic aint it?', video.notes)
        self.assertEqual('W8r-tXRLazs', video.video_id)

    # test bad inputs
    def test_add_video_invalid_url_not_added(self):

        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/watch?soupandsalad1234'
            'https://www.neopets.com',
            'https://www.neopets.com/watch?v='
        ]

        for invalid_video_url in invalid_video_urls:
            
            new_video = {
            'name' : 'example',
            'url' : invalid_video_url,
            'notes': 'isnt ironic aint it?'
            }

            url = reverse('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateNotUsed('video_collection/add.html')

            messages = response.context['messages']
            message_texts = [ message.message for message in messages ]
            
            # getting messaging we'd expect to see from trying to add an invalid video
            self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Please check the data entered', message_texts)

            # database should have no videos
            video_count = Video.objects.count()
            self.assertEqual(0, video_count)


class TestVideoList(TestCase):
    
    def test_all_videos_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='abd', notes='example', url = 'https://www.youtube.com/watch?v=124')
        v2 = Video.objects.create(name='ABBA', notes='example', url = 'https://www.youtube.com/watch?v=125')
        v3 = Video.objects.create(name='YOW', notes='example', url = 'https://www.youtube.com/watch?v=126')
        v4 = Video.objects.create(name='yaw', notes='example', url = 'https://www.youtube.com/watch?v=127')

        expected_video_order = [ v2, v1, v4, v3 ]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['video']) # convert to python list
        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No videos')
        # are there zero videos being sent?
        self.assertEqual(0, len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='abd', notes='example', url = 'https://www.youtube.com/watch?v=124')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_two_videos(self):
        v1 = Video.objects.create(name='abd', notes='example', url = 'https://www.youtube.com/watch?v=124')
        v2 = Video.objects.create(name='jut', notes='example', url = 'https://www.youtube.com/watch?v=129')

        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '2 videos')



class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):
    pass

